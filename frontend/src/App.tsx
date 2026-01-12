import { useState, useEffect } from 'react'
import './App.css'

const API_BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

function App() {
  const [machineCode, setMachineCode] = useState('');
  const [problemCode, setProblemCode] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [library, setLibrary] = useState([]);
  const [isLibraryOpen, setLibraryOpen] = useState(false);
  const [isSaving, setSaving] = useState(false);
  const [saveName, setSaveName] = useState('');
  const [saveDescription, setSaveDescription] = useState('');

  const fetchLibrary = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/get-tms`);
      const data = await response.json();
      setLibrary(data); //library stores all the dictionarys of tms in array
    } catch (error) {
      console.error("Could not load library:", error);
    }
  };


  useEffect(() => {
    fetchLibrary();
  }, []);

  const handleSave = async () => {
      if (!saveName) {
        return alert("Please enter a name for your machine!");
      }
      try {
        const response = await fetch(`${API_BASE_URL}/save-tm-db`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            name: saveName,
            machineCode: machineCode,
            description: saveDescription
          }),
        });

        if (response.ok) {
          alert("Saved successfully!");
          setSaveName('');
          setSaveDescription('');
          setSaving(false);
          fetchLibrary(); //refresh library
        }
      } catch (error) {
        alert("Error saving machine");
      }
    };

    
    const handleRun = async () => {
      setLoading(true);
      try {
        const response = await fetch(`${API_BASE_URL}/run-tm`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            machinecode: machineCode,
            problemcode: problemCode.split(',').map(s => s.trim()) 
          }),
        });

        const data = await response.json();
        setResult(data);
      } 
      catch (error) {
        console.error("Error connecting to backend:", error);
        alert("Backend is not running!");
      }
      finally {
        setLoading(false);
      }
  };

return (
  <div className="container">
    <h1>TM Simulator</h1>
    <button onClick={() => setLibraryOpen(true)}>Open Library</button>
    <details className="hidden-details">
      <summary className="hidden-title">Machine Code Format</summary>
      <pre className="raw-data">
      {`Machine cannot use '*' (wildcard), '_' (blank), ',' (seperation in code) as part of general alphabet
      Line 1: Name,NumTapes,MaxTapeLength,MaxSteps
      Line 2: Input Alphabet (Σ) ex: a,b
      Line 3: State Names ex: q0,q1,accept,reject
      Line 4: Start State Name
      Line 5: AcceptStateName,RejectStateName
      Line 6+: Tape Alphabets (Γ) - one line per tape
      Following Lines: Transitions
      Transition Rule Format: OldState,Input1,Input2,...,NewState,Output1,Output2,...,Direction1,Direction2,...

      Directions can be L for left, R for right, or S for stay

      Example (1-Tape):
      TM-EVEN-LENGTH,1,100,1000
      0,1
      q0,q1,q2,q3
      q0
      q2,q3
      0,1
      q0,*,q1,*,R
      q1,*,q0,*,R
      q0,_,q2,*,R
      q1,_,q3,*,R`}
      </pre>
  </details>

    <textarea
      className="machine-input"
      placeholder="Your Machine Code..." 
      value={machineCode} 
      onChange={(e) => setMachineCode(e.target.value)} 
      rows={10}
    />
    <br/>
    <input
      className="problem-input"
      placeholder="Starting Tape Values... (comma separated)" 
      value={problemCode} 
      onChange={(e) => setProblemCode(e.target.value)} 
    />
    <br/>
    <button className="btn-run" onClick={handleRun} disabled={loading}>{loading ? 'Running Simulation...' : 'Run Simulation'}</button>
    <button onClick={() => setSaving(true)} disabled={loading || !result || result?.status == "error" || result?.data?.error}>Save Current Machine</button>
    {result && (
    <button className="btn-clear" onClick={ () => {setMachineCode(''); setProblemCode(''); setResult(null);}}>Clear</button>
    )}


    {isSaving && (
            <div className="save-dialog">
              <input 
                placeholder="Enter Machine Name..." 
                value={saveName} 
                onChange={(e) => setSaveName(e.target.value)} 
              />
              <textarea 
              className="save-description"
                placeholder="Further Details of the Machine" 
                value={saveDescription} 
                onChange={(e) => setSaveDescription(e.target.value)} 
                rows={3}
              />
              <button onClick={handleSave}>Confirm</button>
              <button onClick={() => setSaving(false)}>Cancel</button>
            </div>
          )}



    {/*This part only shows up after running a machine*/}
      {result && (
        <div className="result-container">
          {result.status === "error" && (
            <div className = "error-text">System Error: {result.message}</div>
          )}

          {result.status === "finished" && (
            <div className="status-card">
            {result.data.error ? (
              <div className = "warning-text">
                <strong>Logic Error:</strong> {result.data.error}
              </div>
            ) : (
              <div className="status-card">
                <h2 className="warning-text">{result.data.machineName}</h2>

                <div className="warning-text">
                  <span className={`badge ${result.data.simulation.status === 'accept' ? 'badge-accept' : 'badge-reject'}`}>
                    {result.data.simulation.status.toUpperCase()}
                  </span>
                  <span className="step-info">
                    <strong>Total Steps:</strong> {result.data.simulation.finalStep}
                  </span>
                </div>

              <strong>Final Tape States:</strong>
                  {result.data.simulation.finalTapes.map((tape: string, tapeNum: number) => (
                    <div key={tapeNum} className="tape-row">
                      <span className="tape-label">Tape {tapeNum + 1}:</span>
                      {tape.replace(/_/g, '\u00A0')}
                    </div>
                  ))}

                <details className="hidden-details">
                  <summary className="hidden-title">View All Steps of Simulation</summary>
                  <pre className="raw-data">
                    {JSON.stringify(result.data, null, 2)}
                  </pre>
                </details>
              </div>
            )}
            </div>
          )}

        </div> 
      )}


  {isLibraryOpen && (
    <div className="modal-overlay">
      <div className="modal-content">
        <div className="modal-header">
          <h2>Community Created Machines</h2>
          <button onClick={() => setLibraryOpen(false)}>Close</button>
        </div>

        <div className="library-grid">
        {library.length === 0 && (
          <div className="warning-text">
            <p>Fetching machines...</p>
        <small>{"If this is taking a while, the Render free tier is likely waking up the backend after inactivity. Please wait up to 1 minute. In the meantime, try creating your own machine! (If being run locally, you haven't saved any machines to your database)"}</small>
        </div>
        )}
          {library.map((m) => (
            <div key={m.id} className="library-card" onClick={() => {
              setMachineCode(m.machineCode);
              setLibraryOpen(false);
            }}>
              <h4>{m.name}</h4>
              <p>{m.description}</p>
              <button className="load-btn">Load Machine</button>
            </div>
          ))}
        </div>
      </div>
    </div>
    )}   
  </div> 
    
  );
}


export default App
