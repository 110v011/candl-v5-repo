import requests
import random

# （中略：url や option の入力部分）

if st.button("ダウンロード準備"):
    if not url:
        st.warning("URLを入力してください。")
    else:
        with st.spinner("今使えるプロキシ（身代わりIP）を探索中..."):
            # 無料のプロキシリストから、有効そうなHTTPプロキシを自動取得する
            proxy_url = None
            try:
                # ProxyScrapeなどの公開APIからプロキシ一覧を取得
                res = requests.get("https://proxyscrape.com")
                if res.status_code == 200 and res.text:
                    proxies = [p.strip() for p in res.text.split("\n") if p.strip()]
                    if proxies:
                        # 取得したリストからランダムに1つ選ぶ
                        selected_proxy = random.choice(proxies)
                        proxy_url = f"http://{selected_proxy}"
                        st.info(f"💡 プロキシを使用します: {selected_proxy}")
            except Exception as proxy_err:
                st.warning("無料プロキシの自動取得に失敗しました。サーバーIPで直接試行します。")

        with st.spinner("動画情報を取得中..."):
            try:
                download_dir = "downloads"
                if not os.path.exists(download_dir):
                    os.makedirs(download_dir)
                
                for f in glob.glob(f"{download_dir}/*"):
                    try: os.remove(f)
                    except: pass

                # 共通オプション
                common_opts = {
                    'extractor_args': {'youtube': {'client': ['ios', 'android']}},
                    'sleep_requests': 2,
                    'source_address': '0.0.0.0',
                    'ignoreerrors': True,
                }

                # プロキシが見つかっていれば設定に追加する
                if proxy_url:
                    common_opts['proxy'] = proxy_url

                # （以下、以前の ydl_opts の処理へ続く...）
