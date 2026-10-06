// React.js dynamic search & quick filter widget for AutoPulse
const { useState, useEffect } = React;

function DealerLiveSearch({ initialDealers }) {
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedState, setSelectedState] = useState('');
  const [dealers, setDealers] = useState(initialDealers || []);

  const filteredDealers = dealers.filter(dealer => {
    const matchesSearch = 
      dealer.full_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      dealer.city.toLowerCase().includes(searchTerm.toLowerCase()) ||
      dealer.short_name.toLowerCase().includes(searchTerm.toLowerCase());
    
    const matchesState = selectedState === '' || dealer.state.toLowerCase() === selectedState.toLowerCase();

    return matchesSearch && matchesState;
  });

  return (
    <div className="card premium-card p-3 mb-4 border-primary border-opacity-25 shadow-sm">
      <div className="d-flex align-items-center justify-content-between mb-3">
        <h6 className="mb-0 fw-bold text-dark d-flex align-items-center gap-2">
          <span className="badge bg-primary rounded-pill">React.js Widget</span>
          <span>Búsqueda Rápida en Vivo</span>
        </h6>
        <span className="text-muted small">
          {filteredDealers.length} concesionario(s) filtrado(s)
        </span>
      </div>

      <div className="row g-2">
        <div className="col-md-8">
          <div className="input-group">
            <span className="input-group-text bg-white"><i className="bi bi-search text-primary"></i></span>
            <input
              type="text"
              className="form-control"
              placeholder="Escribe el nombre del concesionario o ciudad (ej. Wichita, Dallas, Kansas)..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
            {searchTerm && (
              <button className="btn btn-outline-secondary" onClick={() => setSearchTerm('')}>
                ✕
              </button>
            )}
          </div>
        </div>

        <div className="col-md-4">
          <select 
            className="form-select"
            value={selectedState}
            onChange={(e) => setSelectedState(e.target.value)}
          >
            <option value="">Todos los Estados (React)</option>
            <option value="Kansas">Kansas</option>
            <option value="Texas">Texas</option>
            <option value="California">California</option>
            <option value="New York">New York</option>
          </select>
        </div>
      </div>

      {searchTerm && (
        <div className="mt-3">
          <small className="text-muted d-block mb-2">Resultados rápidos en tiempo real:</small>
          <div className="d-flex flex-wrap gap-2">
            {filteredDealers.map(dealer => (
              <a
                key={dealer.id}
                href={`/dealer/${dealer.id}/`}
                className="btn btn-sm btn-outline-primary d-flex align-items-center gap-2 text-start p-2"
                style={{ borderRadius: '8px' }}
              >
                <div>
                  <strong>{dealer.short_name}</strong>
                  <div className="small text-secondary">{dealer.city}, {dealer.state}</div>
                </div>
                <i className="bi bi-arrow-right-short fs-5"></i>
              </a>
            ))}
            {filteredDealers.length === 0 && (
              <span className="text-muted small italic">No hay resultados coincidentes para "{searchTerm}".</span>
            )}
          </div>
        </div>
      )}
    </div>
  );
}

// Mount React widget
document.addEventListener('DOMContentLoaded', () => {
  const container = document.getElementById('react-dealer-filter-root');
  if (container && window.DEALERS_DATA) {
    const root = ReactDOM.createRoot(container);
    root.render(<DealerLiveSearch initialDealers={window.DEALERS_DATA} />);
  }
});
