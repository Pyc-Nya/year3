import express from 'express';
import cors from "cors"

const app = express();
const port = 8000;

const corsOptions = {
  origin: 'http://localhost:5173' 
};

app.use(cors(corsOptions)); 

app.get('/', (req, res) => {
  res.status(404).send('you should not be here');
});

app.get("/api/test_get", (req, res) => {
  res.status(200).send(JSON.stringify({
    data: "hello from server!"
  }))
})

app.listen(port, () => {
  console.log(`Сервер запущен на http://localhost:${port}`);
});