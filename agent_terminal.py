import os
import shutil
from dotenv import load_dotenv
load_dotenv()
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, StorageContext, load_index_from_storage
from llama_index.llms.openai import OpenAI
from utils.file_utils import is_valid_file

# === Load ENV and Validate API Key ===
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    print("Error: OPENAI_API_KEY not found in .env. Please set it.")
    exit(1)

DATA_DIR = "data_input"
PROCESSED_DIR = "processed"
STORAGE_DIR = "storage"
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(PROCESSED_DIR, exist_ok=True)
os.makedirs(STORAGE_DIR, exist_ok=True)

# === Initialize OpenAI LLM correctly ===
llm = OpenAI(api_key=OPENAI_API_KEY, model="gpt-3.5-turbo")

# === Validate and Index Documents ===
valid_files = [
    os.path.join(DATA_DIR, f)
    for f in os.listdir(DATA_DIR)
    if is_valid_file(os.path.join(DATA_DIR, f))[0]
]
for f in os.listdir(DATA_DIR):
    path = os.path.join(DATA_DIR, f)
    _, reason = is_valid_file(path)
    if not is_valid_file(path)[0]:
        print(f"Skipped {f}: {reason}")

if valid_files:
    print(f"Indexing {len(valid_files)} files...")
    docs = SimpleDirectoryReader(input_files=valid_files).load_data()
    index = VectorStoreIndex.from_documents(docs)
    index.storage_context.persist(persist_dir=STORAGE_DIR)
    for f in valid_files:
        try:
            shutil.move(f, os.path.join(PROCESSED_DIR, os.path.basename(f)))
        except Exception as e:
            print(f"Could not move {f}: {e}")
#else:
#    print("Loading existing index...")
#    storage_context = StorageContext.from_defaults(persist_dir=STORAGE_DIR)
#    index = load_index_from_storage(storage_context)
else:
    print("No new valid files found.")

    index_path = os.path.join(STORAGE_DIR, "docstore.json")
    if not os.path.exists(index_path):
        print("❌ Error: No existing index found to load.")
        print("💡 Tip: Add .txt or .pdf files to the 'data_input' folder and run the script again.")
        exit(1)

    print("Loading existing index...")
    storage_context = StorageContext.from_defaults(persist_dir=STORAGE_DIR)
    index = load_index_from_storage(storage_context)

# === Query Engine Setup ===
query_engine = index.as_query_engine(llm=llm)

# === Terminal Chatbot Loop ===
print("\n🤖 Ready to chat! (type 'exit' to quit)")
while True:
    try:
        user_input = input("You> ").strip()
    except (KeyboardInterrupt, EOFError):
        print("\nGoodbye.")
        break

    if user_input.lower() in ("exit", "quit"):
        print("Goodbye.")
        break
    if not user_input:
        print("Please enter something or 'exit' to quit.")
        continue

    response = query_engine.query(user_input)
    print("Agent>", response)
