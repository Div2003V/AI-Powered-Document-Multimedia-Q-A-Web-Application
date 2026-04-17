import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [file, setFile] = useState(null);
  const [question, setQuestion] = useState('');
  const [answer, setAnswer] = useState('');

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  const handleAsk = async () => {
    const formData = new FormData();
    formData.append('file', file);
    await axios.post('http://backend:8000/upload/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });
  };

  const handleQuestionChange = (event) => {
    setQuestion(event.target.value);
  };

  const handleAskQuestion = async () => {
    const response = await axios.post('http://backend:8000/ask/', { question });
    setAnswer(response.data.answer);
  };

  return (
    <div className="App">
      <h1>Document & Multimedia Q&A Web Application</h1>
      <input type="file" onChange={handleFileChange} />
      <button onClick={handleAsk}>Upload</button>
      <br />
      <input type="text" value={question} onChange={handleQuestionChange} placeholder="Ask a question" />
      <button onClick={handleAskQuestion}>Ask</button>
      <p>{answer}</p>
    </div>
  );
}

export default App;
