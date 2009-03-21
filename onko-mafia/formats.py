from formatobjects import filter_weekly, filter_daily, format_spec
import os

def get_json_format():
    return format_spec('{ "week" : %(weekresult)s, "day" : %(dayresult)s }',
        {"weekresult":filter_weekly("true","false"), 
         "dayresult":filter_daily("true","false") })
def get_html_format(locals):
    return format_spec(file(os.path.join(os.path.dirname(__file__),"index.html")).read(),
        {"weekresult":filter_weekly("on","ei"), 
         "dayresult":filter_daily("on","ei"),
         "weekclass":filter_weekly("on","ei"),
         "dayclass":filter_daily("on","ei"),
         "application":locals["application"],
         "project":locals["project"],
         "copyright":locals["copyright"]})
def get_badge_format():
    return format_spec(file(os.path.join(os.path.dirname(__file__),"badge.js")).read(),
        {"weekcolor":filter_weekly("#00ff00","#ff0000"),
         "weekword":filter_weekly("on","ei"),
         "daycolor":filter_daily("#00ff00","#ff0000"),
         "dayword":filter_daily("on","ei")})