<!DOCTYPE html>
<html>
<head>
    <title>画像一覧: {{ url }}</title>
    <link rel="stylesheet" href="/static/style.css">
    <style>
        .image-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
            gap: 10px;
            margin-top: 20px;
        }
        .image-grid img {
            width: 100%;
            height: auto;
            border: 1px solid #ddd;
            border-radius: 4px;
            padding: 5px;
            background-color: #fff;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
    </style>
</head>
<body>
    <h2>{{ url }} から抽出された画像</h2>
    % if error:
        <p class="error">{{ error }}</p>
    % end
    % if not image_urls:
        <p>画像が見つかりませんでした。</p>
    % else:
        <div class="image-grid">
        % for img_url in image_urls:
            <img src="{{ img_url }}" alt="Scraped Image">
        % end
        </div>
    % end
    <br>
    <a href="/" class="back-link">トップに戻る</a>
</body>
</html>