const mongoose = require('mongoose');
const fs = require('fs');
const path = require('path');
require('dotenv').config();

const MONGO_URI = process.env.MONGO_URI || 'mongodb://127.0.0.1:27017/dealershipsDB';

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

async function runSeeder() {
  try {
    await mongoose.connect(MONGO_URI);
    console.log(`Connected to MongoDB for seeding at ${MONGO_URI}`);

    await Dealership.deleteMany({});
    await Review.deleteMany({});

    const dealersRaw = fs.readFileSync(path.join(__dirname, 'data', 'dealerships.json'));
    const dealersData = JSON.parse(dealersRaw);
    await Dealership.insertMany(dealersData);
    console.log(`Successfully seeded ${dealersData.length} dealerships.`);

    const reviewsRaw = fs.readFileSync(path.join(__dirname, 'data', 'reviews.json'));
    const reviewsData = JSON.parse(reviewsRaw);
    await Review.insertMany(reviewsData);
    console.log(`Successfully seeded ${reviewsData.length} reviews.`);

    process.exit(0);
  } catch (err) {
    console.error('Error seeding data:', err);
    process.exit(1);
  }
}

runSeeder();
