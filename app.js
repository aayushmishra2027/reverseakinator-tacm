import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [question, setQuestion] = useState('');
  const [history, setHistory] = useState('');
  const [answers, setAnswers] = useState('');
  const [guess, setGuess] = useState('');
  const [userAnswer, setUserAnswer] = useState('');

  // Handle answer submission
  const handleAnswerSubmit = async () => {
    const updatedHistory = `${history}\nQ: ${question}\nA: ${userAnswer}`;
    setHistory(updatedHistory);
    
    // Get the next question from the API
    const response = await axios.post('http://localhost:5000/generate_question', { history: updatedHistory });
    setQuestion(response.data.question);
    setUserAnswer('');
  };

  // Handle the entity guessing phase
  const handleGuessEntity = async () => {
    const response = await axios.post('http://localhost:5000/guess_entity', { answers: history });
    setGuess(response.data.guess);
  };

  // Start the game
  const startGame = async () => {
    const response = await axios.post('http://localhost:5000/generate_question', { history: '' });
    setQuestion(response.data.question);
  };

  return (
    <div className="App">
      <h1>Reverse Akinator Game</h1>
      {question && !guess ? (
        <>
          <p>{question}</p>
          <input 
            type="text" 
            value={userAnswer} 
            onChange={(e) => setUserAnswer(e.target.value)} 
            placeholder="Yes, No, I don't know..." 
          />
          <button onClick={handleAnswerSubmit}>Submit Answer</button>
          <button onClick={handleGuessEntity}>Make a Guess</button>
        </>
      ) : (
        <>
          {guess && (
            <>
              <h2>My Guess: {guess}</h2>
              <button onClick={startGame}>Play Again</button>
            </>
          )}
        </>
      )}
      <button onClick={startGame}>Start Game</button>
    </div>
  );
}

export default App;
