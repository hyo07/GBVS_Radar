from requests_oauthlib import OAuth1Session
import re
from datetime import datetime, timedelta
from model import session, Tweet
from get_env import get_env

CK = get_env("CONSUMER_KEY")
CS = get_env("CONSUMER_SECRET")
AT = get_env("ACCESS_TOKEN")
ATS = get_env("ACCESS_TOKEN_SECRET")
twitter = OAuth1Session(CK, CS, AT, ATS)

URL = "https://api.twitter.com/1.1/search/tweets.json"

params = {
    "q": "#GBVS対戦募集 exclude:retweets",
    "lang": "ja",
    "result_type": "recent",
    "count": 20,
}


def cut_text(text):
    spl_text = text.split("】")
    return spl_text[-1]


def cut_text_2(text, param):
    text = text.replace("【", "").replace(param, "").replace(":", "").replace("】", "").replace(" ", "")
    return text


def cut_space(text_list: list):
    re_list = []
    for text in text_list:
        re_text = re.sub(r"\s+", " ", text)
        if re_text == " ":
            re_text = ""
        re_list.append(re_text)
    return re_list


recruit_list = []


def get_tweet():
    res = twitter.get(URL, params=params)
    # if res.status_code == 200:
    # tweet = res.json()["statuses"][1]
    for tweet in res.json()["statuses"]:
        # print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        # print()

        tweet_text = tweet["text"].strip("#GBVS対戦募集")

        # print("tweet_text:", tweet_text)
        spl_tweets = tweet_text.split("\n")
        # print("spl_tweets:", spl_tweets)

        extraction_comment = spl_tweets

        param_list = {"player_name": "プレイヤーネーム", "character": "使用キャラ", "rank": "ランク", "vsid": "VSID"}
        content = {}
        flag = True
        for k, v in param_list.items():
            for tw in spl_tweets:
                if v in tw:
                    content[k] = cut_text_2(tw, v)
                    del extraction_comment[spl_tweets.index(tw)]
                    flag = True
                    break
                flag = False
            if not flag:
                # print("不正なツイート")
                break
        if not flag:
            continue

        # if not (content['player_name'] and content["character"] and content["rank"] and content["vsid"]):
        if not content["player_name"]:
            continue

        cuted_space_comment = cut_space(extraction_comment)
        comment_text = "".join(cuted_space_comment)
        content["comment"] = comment_text.replace("【", "").replace("コメント", "").replace(":", "").replace("】", "").strip(
            " ")
        # print("content:", content)

        outer = {"main": content, "rank_tier": None}

        tiers = ["SSS", "SS", "S", "A", "B", "C", "D", "E"]
        full_wdth_tiers = {"ＳＳＳ": "SSS", "ＳＳ": "SS", "Ｓ": "S", "Ａ": "A", "Ｂ": "B", "Ｃ": "C", "Ｄ": "D", "Ｅ": "E"}
        for ti in tiers:
            if ti in content["rank"].upper():
                outer["rank_tier"] = ti
                break
        if not outer["rank_tier"]:
            for fw_ti in full_wdth_tiers.keys():
                if fw_ti in content["rank"]:
                    outer["rank_tier"] = full_wdth_tiers[fw_ti]
                    break

        # outer["character"] = content["character"]
        outer["twitter_id"] = tweet["user"]["screen_name"]
        outer["twitter_name"] = tweet["user"]["name"]
        outer["tweet_id"] = tweet["id_str"]
        outer["datetime"] = datetime.strptime(tweet["created_at"], "%a %b %d %H:%M:%S +0000 %Y") + timedelta(hours=9)

        # print(outer)

        recruit_list.append(outer)
    return recruit_list


def save_tweet():
    tweets = get_tweet()
    for tweet in tweets:
        tweet_id = tweet["tweet_id"]
        if session.query(Tweet).filter(Tweet.tweet_id == tweet_id).first():
            break

        tw = Tweet()
        tw.tweet_id = tweet["tweet_id"]
        tw.twitter_id = tweet["twitter_id"]
        tw.twitter_name = tweet["twitter_name"]
        tw.tweeted_at = tweet["datetime"]
        tw.rank_tier = tweet["rank_tier"]
        tw.player_name = tweet["main"]["player_name"]
        tw.character = tweet["main"]["character"]
        tw.rank = tweet["main"]["rank"]
        tw.vsid = tweet["main"]["vsid"]
        tw.comment = tweet["main"]["comment"]
        session.add(tw)
        session.commit()


if __name__ == "__main__":
    pass

    # print(get_tweet())
    save_tweet()
