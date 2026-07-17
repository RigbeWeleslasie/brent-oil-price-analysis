import { useState, useEffect } from 'react'
import axios from 'axios'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, ReferenceLine } from 'recharts'
import './App.css'

function App() {
  const [prices, setPrices] = useState([])
  const [events, setEvents] = useState([])
  const [changePoints, setChangePoints] = useState(null)
  const [selectedEvents, setSelectedEvents] = useState([])

  useEffect(() => {
    fetchData()
  }, [])

  const fetchData = async () => {
    try {
      const [pricesRes, eventsRes, cpRes] = await Promise.all([
        axios.get('http://127.0.0.1:5000/api/prices'),
        axios.get('http://127.0.0.1:5000/api/events'),
        axios.get('http://127.0.0.1:5000/api/change-points')
      ])

      const chartData = pricesRes.data.dates.map((date, index) => ({
        date: date,
        price: pricesRes.data.prices[index]
      }))

      setPrices(chartData)
      setEvents(eventsRes.data)
      setChangePoints(cpRes.data)
    } catch (error) {
      console.error('Error fetching data:', error)
    }
  }

  const toggleEvent = (event) => {
    if (selectedEvents.find(e => e.date === event.date)) {
      setSelectedEvents(selectedEvents.filter(e => e.date !== event.date))
    } else {
      setSelectedEvents([...selectedEvents, event])
    }
  }

  return (
    <div className="app">
      <header>
        <h1>🛢️ Brent Oil Price Analysis Dashboard</h1>
        <p>Bayesian Change Point Detection & Event Correlation</p>
      </header>

      <div className="dashboard">
        <div className="chart-section">
          <h2>Historical Price Trends</h2>
          <ResponsiveContainer width="100%" height={500}>
            <LineChart data={prices}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="date" tick={{fontSize: 12}} />
              <YAxis label={{ value: 'Price (USD/barrel)', angle: -90, position: 'insideLeft' }} />
              <Tooltip />
              <Legend />
              
              {changePoints && (
                <>
                  <ReferenceLine x={changePoints.single_cp.date} stroke="red" strokeWidth={2} label={{ value: 'Single CP: 2005', position: 'top' }} />
                  <ReferenceLine x={changePoints.two_cp.cp1.date} stroke="orange" strokeWidth={2} label={{ value: '2-CP 1: 2004', position: 'top' }} />
                  <ReferenceLine x={changePoints.two_cp.cp2.date} stroke="purple" strokeWidth={2} label={{ value: '2-CP 2: 2005', position: 'top' }} />
                </>
              )}

              {selectedEvents.map((event, index) => (
                <ReferenceLine 
                  key={index}
                  x={event.date} 
                  stroke="green" 
                  strokeDasharray="5 5"
                  label={{ value: event.event.substring(0, 15) + '...', position: 'top' }}
                />
              ))}

              <Line type="monotone" dataKey="price" stroke="#8884d8" dot={false} strokeWidth={1.5} />
            </LineChart>
          </ResponsiveContainer>
        </div>

        <div className="sidebar">
          <div className="change-points">
            <h3> Detected Change Points</h3>
            {changePoints && (
              <div>
                <div className="cp-card">
                  <h4>Single Model</h4>
                  <p><strong>Date:</strong> {changePoints.single_cp.date}</p>
                  <p><strong>Before:</strong> ${changePoints.single_cp.mu_before}/bbl</p>
                  <p><strong>After:</strong> ${changePoints.single_cp.mu_after}/bbl</p>
                  <p><strong>Impact:</strong> {((changePoints.single_cp.mu_after / changePoints.single_cp.mu_before - 1) * 100).toFixed(0)}% increase</p>
                </div>

                <div className="cp-card">
                  <h4>Two-CP Model</h4>
                  <p><strong>CP1:</strong> {changePoints.two_cp.cp1.date} (${changePoints.two_cp.cp1.mu_before} → ${changePoints.two_cp.cp1.mu_after})</p>
                  <p><strong>CP2:</strong> {changePoints.two_cp.cp2.date} (${changePoints.two_cp.cp2.mu_before} → ${changePoints.two_cp.cp2.mu_after})</p>
                </div>
              </div>
            )}
          </div>

          <div className="events">
            <h3>📅 Historical Events</h3>
            <p className="hint">Click an event to highlight it on the chart</p>
            <div className="event-list">
              {events.map((event, index) => (
                <div 
                  key={index} 
                  className={`event-item ${selectedEvents.find(e => e.date === event.date) ? 'selected' : ''}`}
                  onClick={() => toggleEvent(event)}
                >
                  <strong>{event.date}</strong>
                  <p>{event.event}</p>
                  <span className={`category ${event.category.toLowerCase().replace(' ', '-')}`}>{event.category}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default App
