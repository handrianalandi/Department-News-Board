from nameko.rpc import rpc
import gateway.dependencies.database as database

class NewsService:

    name = "news_service"

    database=database.Database()

    @rpc
    def add_news(self, title, content, user_id,date,file_id):
        return self.database.add_news(title, content, user_id,date,file_id)
    
    @rpc
    def check_news_exist(self, news_id):
        return self.database.check_news_exist(news_id)

    @rpc
    def check_news_belong_to_user(self, news_id, user_id):
        return self.database.check_news_belong_to_user(news_id, user_id)

    @rpc
    def edit_news(self, news_id, title, content,date):
        return self.database.edit_news(news_id, title, content,date)

    @rpc
    def delete_news(self, news_id):
        return self.database.delete_news(news_id)

    @rpc
    def get_news(self):
        return self.database.get_news()

    @rpc
    def get_news_by_id(self, news_id):
        return self.database.get_news_by_id(news_id)

    
        

