<!DOCTYPE html>
<html>
<head>
    <title>NyanchuDaGo検索</title>
    <link rel="stylesheet" href="/static/style.css">
</head>
<body>
    <h2>NyanchuDaGo</h2>
    <form action="/search" method="get">
        <input type="text" name="q" placeholder="検索ワード"><br>
        <label for="region">地域:</label>
        <select name="region" id="region">
            <option value="wt-wt">全世界</option>
            <option value="us-en">米国 (英語)</option>
            <option value="jp-jp">日本 (日本語)</option>
            <!-- Add more regions as needed -->
        </select>
        <label for="timelimit">期間:</label>
        <select name="timelimit" id="timelimit">
            <option value="">すべて</option>
            <option value="d">過去24時間</option>
            <option value="w">過去1週間</option>
            <option value="m">過去1ヶ月</option>
            <option value="y">過去1年</option>
        </select>
        <label for="safesearch">セーフサーチ:</label>
        <select name="safesearch" id="safesearch">
            <option value="moderate">中</option>
            <option value="off">オフ</option>
            <option value="strict">強</option>
        </select><br>
        <input type="submit" value="検索">
    </form>
</body>
</html>
