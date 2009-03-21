class FeedItem:
  def __init__(self,date,weekly):
    self.date=date
    self.day=onko_mafia_day(date)
    self.week=onko_mafia_week(date)
    self.weekly=weekly
  
  def init_feed_dict(self):
    feed_dict={}
    if self.weekly:
      feed_dict["title"]="Onko mafia t&auml;ll&auml; viikolla?"
      feed_dict["answer"]=convert_to_text(self.week)
    else:
      feed_dict["title"]="Onko mafia t&auml;n&auml;&auml;n?"
      feed_dict["answer"]=convert_to_text(self.day)
    feed_dict["date"]=self.date.ctime()
    return feed_dict
    
  def get_rss(self):
    return "<item><title>%(title)s</title><description>%(answer)s</description></item>" % self.init_feed_dict()
    
daydelta=datetime.timedelta(days=1)
weekdelta=7*daydelta

class Feed:
  def __init__(self,count=10,date=None,weekly=False):
    if not date:
      date=datetime.date.today()
    if weekly:
      date=date-date.weekday()*daydelta
    self.items=[]
    for i in range(0,count):
      self.items.append(FeedItem(date),weekly)
      if weekly:
        date=date-weekdelta
      else:
        date=date-daydelta
