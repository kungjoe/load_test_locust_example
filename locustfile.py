from locust import HttpUser, between, task, constant, tag
from pymongo import MongoClient
from time import perf_counter
from uuid_extensions import uuid7, uuid7str
from datetime import datetime


db_name = 'test_db'
db_collection = 'test_collection'

test_messages = '''OpenAI 周四 (15 日) 表示，正在開發一款新的人工智慧 (AI) 模型「Sora」，可透過文字指令來生成短影片，將 AI 技術導入影音領域。
OpenAI 透過部落格文章表示，Sora 可以幫助用戶快速生成長達一分鐘的短影音，創造出具有多個角色、特定運鏡以及精細且複雜的逼真場景，原理類似於 OpenAI 此前開發的 AI 繪圖工具 DALL-E。
OpenAI 執行長奧特曼 (Sam Altman) 在 X 上的一篇文章中寫道，這項工具最開始將提供給「有限的創作者」。該公司同時向一個專家團隊授予訪問權限，負責在正式推出之前評估 Sora 的安全性。
包含 Meta、Alphabet 旗下 Google 和 Runway AI 等公司在內，都曾開發文字轉影音的生成器。Google 在 1 月時推出 Lumiere，AI 新創 Stability AI 也推出名為 table Video Diffusion 的類似產品，亞馬遜的 Create with Alexa 可根據文字指令生成兒童動畫短片。
雖然這項技術可加快創作過程，但也帶來 AI 可能影響藝術家生計與傳播錯誤資訊的疑慮，尤其今年又是關鍵的選舉年。
OpenAI 表示，作為產品推出準備工作的一環，該公司同時也在開發一項工具，幫助偵測 Sora 所生成的影片。'''


class Mongo:
    conn = ""

    def __init__(self):
        # cs = 'mongodb://mongodb-0:27017,mongodb-1:27011,mongodb-2:27012,mongodb-3:27013,mongodb-arbiter-0:27014'
        cs = f"mongodb://localhost:27017"
        self.conn = MongoClient(cs)

    def get_conn(self):
        return self.conn


mongo_client = Mongo()


class MongoUser(HttpUser):

    wait_time = constant(1)

    # @task
    # @tag("GET")
    # def aggregate_test(self):
    #     with mongo_client.get_conn() as cx:
    #         db = cx[db_name]

    #         start_time = perf_counter()

    #         # dummy aggregate example
    #         pipeline = [
    #             {"$unwind": "$tags"},
    #             {"$group": {"_id": "$tags", "count": {"$sum": 1}}},
    #             {"$sort": SON([("count", -1), ("_id", -1)])}
    #         ]
    #         data = list(db[db_collection].aggregate(pipeline))
    #         duration = perf_counter() - start_time

    #         if data:
    #             self.environment.events.request_success.fire(request_type="GET", name="Aggregate test",
    #                                                          response_time=duration, response_length=len(data))
    #         else:
    #             self.environment.events.request_failure.fire(request_type="GET", name="Aggregate test",
    #                                                          response_time=duration, response_length=0)

    # @task
    # @tag("GET")
    # def fetch_test(self):
    #     # with mongo_client.get_conn() as cx:
    #     #     db = cx[db_name]
    #     #     start_time = perf_counter()
    #     #     try:
    #     #         print("start to fetch db")
    #     #         doc_count = db[db_collection].count_documents({})
    #     #         duration = perf_counter() - start_time

    #     #         self.environment.events.request.fire(request_type="GET", name="Fetch documents",
    #     #                                                      response_time=duration, response_length=doc_count)
    #     #     except Exception as e:
    #     #         duration = perf_counter() - start_time
    #     #         print(f"error is {e}")
    #     #         self.environment.events.request.fire(request_type="GET", name="Fetch documents",
    #     #                                                      response_time=duration, response_length=0, exception=e)

    #     cx = mongo_client.get_conn()
    #     db = cx[db_name]
    #     start_time = perf_counter()
    #     try:
    #         print("start to fetch db")
    #         doc_count = db[db_collection].count_documents({})
    #         duration = perf_counter() - start_time

    #         self.environment.events.request.fire(request_type="GET", name="Fetch documents",
    #                                                         response_time=duration, response_length=doc_count)
    #     except Exception as e:
    #         duration = perf_counter() - start_time
    #         print(f"error is {e}")
    #         self.environment.events.request.fire(request_type="GET", name="Fetch documents",
    #                                                         response_time=duration, response_length=0, exception=e)

    @task
    @tag("GET")
    def insert_test(self):

        test_query = {
            'session_id': uuid7str(),
            'messages': test_messages,
            'datetime': datetime.now()
        }

        cx = mongo_client.get_conn()
        db = cx[db_name]
        start_time = perf_counter()
        try:
            print("start to insert to db")
            db[db_collection].insert_one(test_query)
            duration = perf_counter() - start_time

            self.environment.events.request.fire(request_type="GET", name="Insert documents",
                                                            response_time=duration, response_length=0)
        except Exception as e:
            duration = perf_counter() - start_time
            print(f"error is {e}")
            self.environment.events.request.fire(request_type="GET", name="Insert documents",
                                                            response_time=duration, response_length=0, exception=e)
