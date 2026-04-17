from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import whisper
import llamacode
import pymongo
from datetime import datetime

app = FastAPI()

# Initialize Whisper
whisper_model = whisper.load_model("base")

# Initialize llamacode (assuming we have a suitable llamacode library)
llama_model = llamacode.load_model("base")

# Initialize MongoDB
client = pymongo.MongoClient("mongodb://mongo:27017/")
db = client["document_qna_db"]
collection = db["documents"]

class Document(BaseModel):
    name: str
    content: str
    metadata: dict

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    content = await file.read()
    if file.filename.endswith(".pdf"):
        # Convert PDF to text (using an external library like pdfminer)
        text = "PDF to text conversion here"
    elif file.filename.endswith(".mp3") or file.filename.endswith(".mp4"):
        result = whisper_model.transcribe(content)
        text = result["text"]
    else:
        return JSONResponse(content={"error": "Unsupported file type"}, status_code=400)

    document = {
        "name": file.filename,
        "content": text,
        "metadata": {
            "upload_time": datetime.now().isoformat(),
            "file_type": file.filename.split(".")[-1]
        }
    }
    collection.insert_one(document)

    return JSONResponse(content={"message": "File uploaded successfully"})

@app.post("/ask/")
async def ask_question(question: str):
    response = llama_model.ask(question)
    answer = response.choices[0].text.strip()
    return JSONResponse(content={"answer": answer})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
