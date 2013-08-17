# DailyKindle

将RSS生成Kindle上阅读的.mobi文件，不支持图片。

GitHub上有另外一个项目叫[kindlereader](https://github.com/williamgateszhao/kindlereader), 
干的事情基本相同，不过代码太复杂以及不优美，于是fork了这个项目并且做了很多修改，很简单。

## 使用

安装[Amazon's KindleGen](http://www.amazon.com/gp/feature.html?docId=1000234621)，在`config.py`中填写配置，运行(python3)。

## Crontab Example

`50 7 * * * LANG=en_US.UTF-8 timeout 120 python /path/to/dailykindle.py`

## License

Have fun.
