<!DOCTYPE html>
<html>
<head>
    <title>検索結果: {{ query }}</title>
    <link rel="stylesheet" href="/static/style.css">
</head>
<body>
    <h2>検索結果: {{ query }}</h2>
    <div class="search-options">
        % if region:
            地域: {{ region }}
        % end
        % if timelimit:
            期間: {{ timelimit }}
        % end
        % if safesearch:
            セーフサーチ: {{ safesearch }}
        % end
    </div>
    % if error:
        <p class="error">{{ error }}</p>
    % end
    % if not results:
        <p>検索結果が見つかりませんでした。</p>
    % else:
        <ul>
        % for result in results:
            <li>
                <a href="{{ result.get('href') or result.get('url') }}" target="_blank">
                    <strong>{{ result.get('title', 'No Title') }}</strong>
                </a>
                <p class="snippet">{{ result.get('body', '') }}</p>
                <p><a href="/all_image?url={{ result.get('href') or result.get('url') }}">このサイトの画像をすべて表示</a></p>
            </li>
        % end
        </ul>
    % end
    <br>
    <a href="/" class="back-link">トップに戻る</a>
</body>
</html>