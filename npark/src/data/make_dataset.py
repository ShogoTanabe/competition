import pandas as pd 
import numpy as np 


def format_train(train_raw):
  _train = train_raw.copy()

  # Datetime index
  _train.index = pd.to_datetime(_train.index)

  # from park to park_cate 
  parkDict = {park:i for i, park in enumerate(_train.park.unique())}
  _train["park_cate"] = _train["park"].map(parkDict)

  return _train, parkDict



def format_weather(weather_raw):
  _weather = weather_raw.copy()

  _weather.index = pd.to_datetime(_weather.index)
  _weather.index.name = "datetime"

  # from 地点 to park_cate
  weatherDict = {
  '十和田': 1, '大山': 4, '大田': 4, '日光': 2, '渡嘉敷': 7, '熊本': 5,
  '釧路': 0, '青森': 1, '高森': 5, '鳥羽': 3, '鹿児島': 6, '鹿角': 1,
  }
  _weather["park_cate"] = _weather["地点"].map(weatherDict)


  return _weather, weatherDict


def format_holiday(holiday_raw):
  _holiday = holiday_raw.copy()

  _holiday.drop(["年号", "和暦", "曜日", "曜日番号"], axis=1, inplace=True)

  _holiday.columns = ["year", "month", "day", "is_holiday"]


  # 祝日設定
  _holiday.fillna(0, inplace=True)
  _holiday["is_holiday"].where(_holiday["is_holiday"] == 0, 1, inplace=True) 
  _holiday["is_holiday"] = _holiday["is_holiday"].astype(np.int64)

### 追加変数 ###

  # 祝前/後日
  _holiday["prev_day_is_holiday"] = _holiday["is_holiday"].shift()
  _holiday["next_day_is_holiday"] = _holiday["is_holiday"].shift(-1)

  # 祝日 + 前日
  _holiday["prev_day_is_holiday & is_holiday"] = _holiday["prev_day_is_holiday"] + _holiday["is_holiday"]

  # 祝日 + 後日
  _holiday["next_day_is_holiday & is_holiday"] = _holiday["next_day_is_holiday"] + _holiday["is_holiday"]

  # 祝日 + 前日 + 後日
  _holiday["prev_day_is_holiday & next_day_is_holiday & is_holiday"] = _holiday["prev_day_is_holiday"] + _holiday["is_holiday"] + _holiday["next_day_is_holiday"]

  ## 夏休み
  _holiday["natsu-yasumi"] = 0
  _holiday["natsu-yasumi"].mask( (_holiday["month"] == 7) & (_holiday["day"]  > 25), 1, inplace=True)
  _holiday["natsu-yasumi"].mask( (_holiday["month"] == 8) & (_holiday["day"]  < 30), 1, inplace=True)

  ## 冬休み
  _holiday["fuyu-yasumi"] = 0
  _holiday["fuyu-yasumi"].mask( (_holiday["month"] == 12) & (_holiday["day"] > 20), 1, inplace=True)
  _holiday["fuyu-yasumi"].mask( (_holiday["month"] == 1) & (_holiday["day"] < 9), 1, inplace=True)

  ## 春休み
  _holiday["haru-yasumi"] = 0
  _holiday["haru-yasumi"].mask( (_holiday["month"] == 3) & (_holiday["day"] > 20), 1, inplace=True)
  _holiday["haru-yasumi"].mask( (_holiday["month"] == 4) & (_holiday["day"] < 9), 1, inplace=True)

  ## ゴールデンウィーク
  _holiday["gWeek"] = 0
  _holiday["gWeek"].mask( (_holiday["month"] == 4) & (_holiday["day"] > 26), 1, inplace=True)
  _holiday["gWeek"].mask( (_holiday["month"] == 5) & (_holiday["day"] < 6), 1, inplace=True)

  ## シルバーウィーク
  _holiday["sWeek"] = 0
  _holiday["sWeek"].mask( (_holiday["month"] == 9) & ( (_holiday["day"] > 15) & (_holiday["day"] < 26) ), 1, inplace=True)

  ## お盆
  _holiday["obon"] = 0
  _holiday["obon"].mask( (_holiday["month"] == 8) & ( (_holiday["day"] > 10) & (_holiday["day"] < 18) ), 1, inplace=True)

  ## 年末年始
  _holiday["nenmatsu-nenshi"] = 0
  _holiday["nenmatsu-nenshi"].mask( (_holiday["month"] == 12) & (_holiday["day"] == 31), 1, inplace=True)
  _holiday["nenmatsu-nenshi"].mask( (_holiday["month"] == 1) & (_holiday["day"] < 4), 1, inplace=True)

  ## gWeek + sWeek
  _holiday["gWeek & sWeek"] = _holiday["gWeek"] + _holiday["sWeek"]

  ## gWeek + sWeek + お盆 + 年末年始
  _holiday["gWeek & sWeek & obon & nenmatsu-nenshi"] = _holiday["gWeek"] + _holiday["sWeek"] + _holiday["obon"] + _holiday["nenmatsu-nenshi"]

  ## 長期休み
  _holiday["natsu-yasumi & fuyu-yasumi & haru-yasumi"] = _holiday["natsu-yasumi"] + _holiday["fuyu-yasumi"] + _holiday["haru-yasumi"]


  print(_holiday.shape)
  return _holiday



