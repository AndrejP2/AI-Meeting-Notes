import { useState } from "react";
import "./App.css";

function App() {
  const [text, setText] = useState("");
  const [result, setResult] = useState(null);
  const [meetings, setMeetings] = useState([]);
  const [loading, setLoading] = useState(false);

  const analyzeText = async () => {
    if (!text.trim()) return;

    setLoading(true);

    const response = await fetch("http://localhost:8000/analyze-text", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        text: text,
      }),
    });

    const data = await response.json();

    setResult(data);
    setText("");
    setLoading(false);

    loadMeetings();
  };

  const loadMeetings = async () => {
    const response = await fetch("http://localhost:8000/meetings");
    const data = await response.json();

    setMeetings(data);
  };

  const deleteMeeting = async (id) => {
    await fetch(`http://localhost:8000/meetings/${id}`, {
      method: "DELETE",
    });

    loadMeetings();
  };

  return (
    <div className="page">
      <div className="container">

        <header className="header">
          <div>
            <p className="eyebrow">LOCAL AI WORKSPACE</p>
            <h1>Meeting Notes</h1>
            <p className="subtitle">
              Pretvori zapis sastanka u jasan sažetak, ključne točke i zadatke.
            </p>
          </div>

          <div className="status">
            <span className="status-dot"></span>
            Local AI
          </div>
        </header>

        <main>
          <section className="input-card">
            <div className="section-heading">
              <div>
                <h2>Analiziraj sastanak</h2>
                <p>Zalijepi tekst sastanka ispod.</p>
              </div>
            </div>

            <textarea
              value={text}
              onChange={(e) => setText(e.target.value)}
              placeholder="Primjer: Na današnjem sastanku dogovorili smo..."
            />

            <div className="input-footer">
              <span>{text.length} znakova</span>

              <button
                className="primary-button"
                onClick={analyzeText}
                disabled={loading || !text.trim()}
              >
                {loading ? "Analiziram..." : "Analiziraj"}
              </button>
            </div>
          </section>

          {result && (
            <section className="results">
              <div className="result-card result-main">
                <span className="card-label">SAŽETAK</span>
                <h2>Pregled sastanka</h2>
                <p>{result.summary}</p>
              </div>

              <div className="result-grid">
                <div className="result-card">
                  <span className="card-label">KLJUČNE RIJEČI</span>

                  <div className="tags">
                    {result.keywords.map((keyword, index) => (
                      <span className="tag" key={index}>
                        {keyword}
                      </span>
                    ))}
                  </div>
                </div>

                <div className="result-card">
                  <span className="card-label">GLAVNE TOČKE</span>

                  <ul className="clean-list">
                    {result.main_points.map((point, index) => (
                      <li key={index}>{point}</li>
                    ))}
                  </ul>
                </div>

                <div className="result-card full-width">
                  <span className="card-label">ZADACI</span>

                  {result.action_items.length > 0 ? (
                    <ul className="action-list">
                      {result.action_items.map((item, index) => (
                        <li key={index}>
                          <span className="check">✓</span>
                          {item}
                        </li>
                      ))}
                    </ul>
                  ) : (
                    <p className="muted">Nema pronađenih zadataka.</p>
                  )}
                </div>
              </div>
            </section>
          )}

          <section className="saved-section">
            <div className="saved-header">
              <div>
                <p className="eyebrow">POVIJEST</p>
                <h2>Spremljeni sastanci</h2>
              </div>

              <button
                className="secondary-button"
                onClick={loadMeetings}
              >
                Učitaj sastanke
              </button>
            </div>

            {meetings.length === 0 ? (
              <div className="empty-state">
                Još nema učitanih sastanaka.
              </div>
            ) : (
              <div className="meeting-list">
                {meetings.map((meeting) => (
                  <div className="meeting-item" key={meeting.id}>
                    <div className="meeting-number">
                      {meeting.id}
                    </div>

                    <div className="meeting-content">
                      <h3>{meeting.summary}</h3>

                      <p>
                        {meeting.keywords?.slice(0, 4).join(" · ")}
                      </p>
                    </div>

                    <button
                      className="delete-button"
                      onClick={() => deleteMeeting(meeting.id)}
                    >
                      Obriši
                    </button>
                  </div>
                ))}
              </div>
            )}
          </section>
        </main>

      </div>
    </div>
  );
}

export default App;