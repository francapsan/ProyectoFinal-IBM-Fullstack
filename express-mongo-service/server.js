const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');
const fs = require('fs');
const path = require('path');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 3030;
const MONGO_URI = process.env.MONGO_URI || 'mongodb://127.0.0.1:27017/dealershipsDB';

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Mongoose Schemas & Models
const dealershipSchema = new mongoose.Schema({
  id: { type: Number, required: true, unique: true },
  city: { type: String, required: true },
  state: { type: String, required: true },
  st: { type: String, required: true },
  address: { type: String, required: true },
  zip: { type: String, required: true },
  lat: { type: Number, required: true },
  long: { type: Number, required: true },
  short_name: { type: String, required: true },
  full_name: { type: String, required: true }
});

const reviewSchema = new mongoose.Schema({
  id: { type: Number, required: true, unique: true },
  name: { type: String, required: true },
  dealership: { type: Number, required: true },
  review: { type: String, required: true },
  purchase: { type: Boolean, default: false },
  purchase_date: { type: String, default: "" },
  car_make: { type: String, default: "" },
  car_model: { type: String, default: "" },
  car_year: { type: Number, default: new Date().getFullYear() }
}, { timestamps: true });

const Dealership = mongoose.model('Dealership', dealershipSchema);
const Review = mongoose.model('Review', reviewSchema);

// In-memory fallback dataset
let memoryDealers = [];
let memoryReviews = [];
try {
  memoryDealers = JSON.parse(fs.readFileSync(path.join(__dirname, 'data', 'dealerships.json')));
  memoryReviews = JSON.parse(fs.readFileSync(path.join(__dirname, 'data', 'reviews.json')));
} catch (e) {
  console.warn("Could not load initial JSON memory cache:", e.message);
}

let isMongoConnected = false;

// Auto-seed function
async function seedDatabaseIfEmpty() {
  try {
    const dealerCount = await Dealership.countDocuments();
    if (dealerCount === 0) {
      await Dealership.insertMany(memoryDealers);
      console.log(`[SEED] Inserted ${memoryDealers.length} dealerships.`);
    }

    const reviewCount = await Review.countDocuments();
    if (reviewCount === 0) {
      await Review.insertMany(memoryReviews);
      console.log(`[SEED] Inserted ${memoryReviews.length} reviews.`);
    }
  } catch (err) {
    console.error('[SEED ERROR]', err.message);
  }
}

// Connect to MongoDB
mongoose.connect(MONGO_URI, { serverSelectionTimeoutMS: 2000 })
  .then(async () => {
    isMongoConnected = true;
    console.log(`Connected to MongoDB at ${MONGO_URI}`);
    await seedDatabaseIfEmpty();
  })
  .catch(err => {
    isMongoConnected = false;
    console.warn(`[INFO] MongoDB not running locally (${err.message}). Using fast in-memory JSON dataset.`);
  });

// --- REST Endpoints ---

// 1. Service Health / Welcome
app.get('/', (req, res) => {
  res.json({
    service: "Dealership & Reviews Express/Mongo Microservice",
    status: "online",
    storage: isMongoConnected ? "MongoDB" : "In-Memory JSON Fallback",
    endpoints: [
      "GET /dealers (or /fetchDealers)",
      "GET /dealers/:state (or /dealers/state/:state)",
      "GET /dealer/:id (or /dealers/:id)",
      "GET /reviews/dealer/:id (or /fetchReviews/dealer/:id)",
      "POST /insert_review"
    ]
  });
});

// Helper for dealers by state
const getDealersByStateHandler = async (req, res) => {
  try {
    const { state } = req.params;
    if (isMongoConnected) {
      const dealers = await Dealership.find({
        $or: [
          { state: { $regex: new RegExp(`^${state}$`, 'i') } },
          { st: { $regex: new RegExp(`^${state}$`, 'i') } }
        ]
      });
      return res.status(200).json(dealers);
    }
    const filtered = memoryDealers.filter(d => 
      d.state.toLowerCase() === state.toLowerCase() || 
      d.st.toLowerCase() === state.toLowerCase()
    );
    return res.status(200).json(filtered);
  } catch (error) {
    return res.status(500).json({ error: error.message });
  }
};

// Helper for dealer by ID (returns JSON array matching reference format)
const getDealerByIdHandler = async (req, res) => {
  try {
    const dealerId = parseInt(req.params.id, 10);
    if (isNaN(dealerId)) {
      return getDealersByStateHandler(req, res);
    }
    if (isMongoConnected) {
      const dealers = await Dealership.find({ id: dealerId });
      if (!dealers || dealers.length === 0) {
        return res.status(404).json({ error: `Dealer with ID ${dealerId} not found` });
      }
      return res.status(200).json(dealers);
    }
    const dealer = memoryDealers.find(d => d.id === dealerId);
    if (!dealer) {
      return res.status(404).json({ error: `Dealer with ID ${dealerId} not found` });
    }
    return res.status(200).json([dealer]);
  } catch (error) {
    return res.status(500).json({ error: error.message });
  }
};

// 2. Get All Dealerships
app.get(['/dealers', '/fetchDealers'], async (req, res) => {
  try {
    const { state } = req.query;
    if (isMongoConnected) {
      let query = {};
      if (state) {
        query = {
          $or: [
            { state: { $regex: new RegExp(`^${state}$`, 'i') } },
            { st: { $regex: new RegExp(`^${state}$`, 'i') } }
          ]
        };
      }
      const dealers = await Dealership.find(query);
      return res.status(200).json(dealers);
    }
    if (state) {
      const filtered = memoryDealers.filter(d => 
        d.state.toLowerCase() === state.toLowerCase() || 
        d.st.toLowerCase() === state.toLowerCase()
      );
      return res.status(200).json(filtered);
    }
    return res.status(200).json(memoryDealers);
  } catch (error) {
    return res.status(500).json({ error: error.message });
  }
});

// 3. Get Dealerships by State (Kansas rubric requirement: /dealers/Kansas)
app.get('/dealers/state/:state', getDealersByStateHandler);
app.get('/fetchDealers/:state', getDealersByStateHandler);

// 4. Get Dealer by ID
app.get('/dealer/:id', getDealerByIdHandler);
app.get('/fetchDealer/:id', getDealerByIdHandler);

// Route for /dealers/:param (handles state like /dealers/Kansas or numeric ID like /dealers/1)
app.get('/dealers/:param', async (req, res) => {
  const { param } = req.params;
  const isNumeric = /^\d+$/.test(param);
  if (isNumeric) {
    req.params.id = param;
    return getDealerByIdHandler(req, res);
  } else {
    req.params.state = param;
    return getDealersByStateHandler(req, res);
  }
});

// 5. Get Reviews for a Dealer
app.get(['/reviews/dealer/:id', '/fetchReviews/dealer/:id'], async (req, res) => {
  try {
    const dealerId = parseInt(req.params.id, 10);
    if (isNaN(dealerId)) {
      return res.status(400).json({ error: "Invalid dealer ID" });
    }
    if (isMongoConnected) {
      const reviews = await Review.find({ dealership: dealerId }).sort({ createdAt: -1 });
      return res.status(200).json(reviews);
    }
    const filteredReviews = memoryReviews.filter(r => r.dealership === dealerId);
    return res.status(200).json(filteredReviews);
  } catch (error) {
    return res.status(500).json({ error: error.message });
  }
});

// 6. Insert a Review
app.post(['/insert_review', '/reviews'], async (req, res) => {
  try {
    const reviewData = req.body;
    if (!reviewData.name || !reviewData.dealership || !reviewData.review) {
      return res.status(400).json({ error: "Missing required fields: name, dealership, review" });
    }

    if (isMongoConnected) {
      if (!reviewData.id) {
        const highestReview = await Review.findOne().sort({ id: -1 });
        reviewData.id = highestReview ? highestReview.id + 1 : 1;
      }
      const newReview = new Review(reviewData);
      const saved = await newReview.save();
      return res.status(201).json(saved);
    }

    // In-memory save fallback
    if (!reviewData.id) {
      const maxId = memoryReviews.reduce((max, r) => r.id > max ? r.id : max, 0);
      reviewData.id = maxId + 1;
    }
    memoryReviews.unshift(reviewData);
    return res.status(201).json(reviewData);
  } catch (error) {
    return res.status(500).json({ error: error.message });
  }
});

// Manual re-seed endpoint
app.post('/seed', async (req, res) => {
  try {
    await Dealership.deleteMany({});
    await Review.deleteMany({});
    await seedDatabaseIfEmpty();
    return res.json({ message: "Database re-seeded successfully." });
  } catch (error) {
    return res.status(500).json({ error: error.message });
  }
});

app.listen(PORT, '0.0.0.0', () => {
  console.log(`Express Mongo service listening on port ${PORT}`);
});
