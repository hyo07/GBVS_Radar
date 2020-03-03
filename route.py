from flask import Flask, render_template, request
from model import session, Tweet
from sqlalchemy import desc
from datetime import datetime

app = Flask(__name__)


def parse_elapsed(dt):
    if "day" in dt:
        num = dt.split("day")[0].replace(" ", "")
        return num + "日"
    else:
        spl_time = dt.split(":")
        if spl_time[0] == "0":
            return spl_time[1] + "分"
        else:
            return spl_time[0] + "時間"


@app.route("/")
def index():
    tweets_json = []
    tier_dic = {
        "": {"checked": False, "rank": "", "name": "全て"},
        "SSSS": {"checked": False, "rank": "SSSS", "name": "SSSS"},
        "SSS": {"checked": False, "rank": "SSS", "name": "SSS"},
        "SS": {"checked": False, "rank": "SS", "name": "SS"},
        "S": {"checked": False, "rank": "S", "name": "S"},
        "A": {"checked": False, "rank": "A", "name": "A"},
        "B": {"checked": False, "rank": "B", "name": "B"},
        "C": {"checked": False, "rank": "C", "name": "C"},
        "D": {"checked": False, "rank": "D", "name": "D"},
        "E": {"checked": False, "rank": "E", "name": "E"},
    }
    chara_dic = {
        "": {"checked": False, "character": "", "name": "全て"},
        "グラン": {"checked": False, "character": "グラン", "name": "グラン"},
        "カタリナ": {"checked": False, "character": "カタリナ", "name": "カタリナ"},
        "シャル": {"checked": False, "character": "シャル", "name": "シャル"},
        "ランス": {"checked": False, "character": "ランス", "name": "ランス"},
        "パー": {"checked": False, "character": "パー", "name": "パー"},
        "フェリ": {"checked": False, "character": "フェリ", "name": "フェリ"},
        "ローアイン": {"checked": False, "character": "ローアイン", "name": "ローアイン"},
        "ファスティバ": {"checked": False, "character": "ファスティバ", "name": "ファスティバ"},
        "メーテラ": {"checked": False, "character": "メーテラ", "name": "メーテラ"},
        "ゼタ": {"checked": False, "character": "ゼタ", "name": "ゼタ"},
        "バザラガ": {"checked": False, "character": "バザラガ", "name": "バザラガ"},
        "ベルゼバブ": {"checked": False, "character": "ベル", "name": "ベルゼバブ"},
        "ナルメア": {"checked": False, "character": "ナルメア", "name": "ナルメア"},
    }

    dt_now = datetime.now()
    tier = request.args.get("rank_tiers")
    character = request.args.get("character")

    if tier and character:
        tweets = session.query(Tweet).filter(
            Tweet.rank_tier == tier, Tweet.character.like("%{}%".format(character))
        ).order_by(desc(Tweet.tweeted_at)).limit(20).offset(0).all()
        tier_dic[tier]["checked"] = True
        chara_dic[character]["checked"] = True


    elif (not tier) and character:
        tweets = session.query(Tweet).filter(
            Tweet.character.like("%{}%".format(character))
        ).order_by(desc(Tweet.tweeted_at)).limit(20).offset(0).all()
        tier_dic[""]["checked"] = True
        chara_dic[character]["checked"] = True


    elif tier and (not character):
        tweets = session.query(Tweet).filter(
            Tweet.rank_tier == tier
        ).order_by(desc(Tweet.tweeted_at)).limit(20).offset(0).all()
        tier_dic[tier]["checked"] = True
        chara_dic[""]["checked"] = True

    else:
        tweets = session.query(Tweet).order_by(desc(Tweet.tweeted_at)).limit(20).offset(0).all()
        tier_dic[""]["checked"] = True
        chara_dic[""]["checked"] = True

    for tweet in tweets:
        tweets_json.append(
            {
                "tweet_id": tweet.tweet_id,
                "twitter_id": tweet.twitter_id,
                "twitter_name": tweet.twitter_name,
                "tweeted_at": tweet.tweeted_at,
                "rank_tier": tweet.rank_tier,
                "player_name": tweet.player_name,
                "character": tweet.character,
                "rank": tweet.rank,
                "vsid": tweet.vsid,
                "comment": tweet.comment,
                "elapsed_time": parse_elapsed(str(dt_now - tweet.tweeted_at))
            }
        )
    return render_template("index.html", tweets=tweets_json, tiers=tier_dic, characters=chara_dic)


if __name__ == "__main__":
    app.run(host="localhost", port=8000, debug=True)
    # app.run(host="0.0.0.0", port=8000, debug=False)
