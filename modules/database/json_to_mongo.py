import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))


from typing import Union, List, Dict, Any
from urllib.parse import quote_plus
from pymongo import MongoClient
from dateutil.parser import parse
from modules.json_manager import JSONManager



class JsonToMongo:
    def __init__(
        self,
        mongo_uri: str,
        db_name: str,
        collection_name: str,
        input_path: Union[str, List[str]],
        batch_size: int = 100,
        drop: bool = False,
        flag_timestamp: bool = False,
        timestamp_field: str = "timestamp",
        delete_input_file_on_success: bool = False
    ):
        self.input_file_paths = JSONManager.resolve_json_files(input_path)
        self.mongo_uri = mongo_uri
        self.db_name = db_name
        self.collection_name = collection_name
        self.batch_size = batch_size
        self.flag_timestamp = flag_timestamp
        self.timestamp_field = timestamp_field
        self.drop = drop
        self.delete_input_file_on_success = delete_input_file_on_success

        # Mongo
        self.client = None
        self.collection = None


        #processing status variables
        self.total_files = len(self.input_file_paths)
        self.current_file = ""
        self.total_records = 0
        self.processed_files = 0
        self.success_count = 0
        self.errors = 0

    def _print_status(self):
        os.system("cls" if os.name == "nt" else "clear")
        print("📊 Mongo Import Status (JsonToMongo):")
        print(f"    📂 Current File: {self.current_file}")
        print(f"    📍 Processed Files: {self.processed_files}/{self.total_files}")
        print(f"    ✅ Inserted Records: {self.success_count}")
        print(f"    ❌ Errors: {self.errors}")
        print("-------------------------------------------------------------")







    def _connect(self):
        try:
            self.client = MongoClient(self.mongo_uri)
            self.collection = self.client[self.db_name][self.collection_name]
            print("✅ Connected to MongoDB")
        except Exception as e:
            print(f"❌ MongoDB Connection Error: {e}")
            self.errors += 1

    def _drop_collection(self):
        try:
            self.collection.drop()
            print(f"🧹 Collection '{self.collection_name}' dropped.")
        except Exception as e:
            print(f"❌ Drop Collection Error: {e}")
            self.errors += 1

    def _convert_timestamp(self, item: Dict[str, Any]) -> Dict[str, Any]:
        if self.timestamp_field in item and isinstance(item[self.timestamp_field], str):
            try:
                item[self.timestamp_field] = parse(item[self.timestamp_field])
            except Exception:
                pass
        return item

    def _insert_batch(self, data: List[Dict[str, Any]]) -> bool:
        try:
            result = self.collection.insert_many(data)
            self.success_count += len(result.inserted_ids)
            self.total_records += len(result.inserted_ids)
            print(f"✅ Inserted {len(result.inserted_ids)} documents.")
            return True
        except Exception as e:
            print(f"❌ Insert Error: {e}")
            self.errors += 1
            return False

    def _delete_file(self, file_path: str):
        try:
            os.remove(file_path)
            print(f"🗑️ Deleted file: {file_path}")
        except Exception as e:
            print(f"❌ File deletion error: {e}")
            self.errors += 1





    def run(self):
        self._connect()
        if self.collection is None:
            print("❌ Mongo connection failed. Aborting.")
            return

        if self.drop:
            self._drop_collection()

        batch = []
        files_to_delete = []

        for file_path in self.input_file_paths:
            self.current_file = file_path
            data = JSONManager.load_json_as_list(file_path)
            self.processed_files += 1

            if not data:
                continue

            for record in data:
                if self.flag_timestamp:
                    record = self._convert_timestamp(record)
                batch.append(record)

            files_to_delete.append(file_path)

            if len(batch) >= self.batch_size:
                success = self._insert_batch(batch)
                if success and self.delete_input_file_on_success:
                    for path in files_to_delete:
                        self._delete_file(path)
                batch.clear()
                files_to_delete.clear()
                self._print_status()

        # Final flush
        if batch:
            success = self._insert_batch(batch)
            if success and self.delete_input_file_on_success:
                for path in files_to_delete:
                    self._delete_file(path)
            self._print_status()

        if self.client:
            self.client.close()
            print("🔒 MongoDB connection closed")






    
if __name__ == "__main__":
    MONGODB_CONFIG = {
        "username": "fardad", 
        "password": quote_plus("StrongPassword12Wee%%%%&&3!"), 
        "host": "92.205.191.109",
        "port": "27017", 
        "auth_db": "admin",
        "db_name": "shop",
    }

    config = {
        "mongo_uri": f"mongodb://{MONGODB_CONFIG['username']}:{MONGODB_CONFIG['password']}@{MONGODB_CONFIG['host']}:{MONGODB_CONFIG['port']}/?authSource={MONGODB_CONFIG['auth_db']}",
        "db_name": "shop",
        "collection_name": "foodhub_datamining_resid",
        "input_path": "data",
        "drop": False,
        "flag_timestamp": False,
        "timestamp_field": "",
        "delete_input_file_on_success": False,
        "batch_size": 100,
    }

    JsonToMongo(**config).run()
