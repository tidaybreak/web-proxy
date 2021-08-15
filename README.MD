export APP_CONFIG=HaoMengAd
export APP_CONFIG=Hnputihd


docker stop web-proxy
docker rm web-proxy
docker run --name web-proxy -d \
--restart=always \
-e PYTHONUNBUFFERED=1 \
-e TERM=linux \
-e C_FORCE_ROOT=true \
-e APP_CONFIG= \
--net mynet \
--ip 172.18.0.135 \
--mount type=bind,source=/etc/resolv.docker.conf,target=/etc/resolv.conf \
--mount type=bind,source=/home/data/docker-volume/web-proxy/,target=/opt/app-root/src \
centos/python-36-centos7:latest \
/bin/sh /opt/app-root/src/run.sh


# 关键字替换
grep "友盟" * -R | awk -F: '{print $1}' | sort | uniq | xargs sed -i 's/友盟/昊盟/g'
grep "盛赫" * -R | awk -F: '{print $1}' | sort | uniq | xargs sed -i 's/盛赫/昊盟/g'
grep "吞噬" * -R | awk -F: '{print $1}' | sort | uniq | xargs sed -i 's/吞噬/昊盟/g'
grep "行为洞察" * -R | awk -F: '{print $1}' | sort | uniq | xargs sed -i 's/行为洞察/游戏洞察/g'
grep "人群洞察" * -R | awk -F: '{print $1}' | sort | uniq | xargs sed -i 's/人群洞察/数据洞察/g'
grep "用户生命周期" * -R | awk -F: '{print $1}' | sort | uniq | xargs sed -i 's/用户生命周期/榜单监控/g'


# src="//
grep 'src="//' * -R | awk -F: '{print $1}' | sort | uniq | xargs sed -i 's/src="\/\//src="\//g'
# src="https://
grep 'src="https://' * -R | awk -F: '{print $1}' | sort | uniq | xargs sed -i 's/src="https:\/\//src="\//g'
# href="//
grep 'href="//' * -R | awk -F: '{print $1}' | sort | uniq | xargs sed -i 's/href="\/\//href="\//g'
# href="https://
grep 'href="https://' * -R | awk -F: '{print $1}' | sort | uniq | xargs sed -i 's/href="https:\/\//href="\//g'
# url(//
grep 'url(//' * -R | awk -F: '{print $1}' | sort | uniq | xargs sed -i 's/url(\/\//url(\//g'
# url(\'//
grep 'url(\\'"'"'//' * -R | awk -F: '{print $1}' | sort | uniq | xargs sed -i 's/url(\\'"'"'\/\//url(\\'"'"'\//g'


grep '"//workbench.umeng.com' * -R | awk -F: '{print $1}' | sort | uniq | xargs sed -i 's/"\/\/workbench.umeng.com/"\/workbench.umeng.com/g'
grep '"//mobile.umeng.com' * -R | awk -F: '{print $1}' | sort | uniq | xargs sed -i 's/"\/\/mobile.umeng.com/"/g'
grep '"//g.alicdn.com' * -R | awk -F: '{print $1}' | sort | uniq | xargs sed -i 's/"\/\/g.alicdn.com/"\/g.alicdn.com/g'
grep '"https://g.alicdn.com' * -R | awk -F: '{print $1}' | sort | uniq | xargs sed -i 's/https:\/\/g.alicdn.com/\/g.alicdn.com/g'
grep 'https://bizport.umeng.com' * -R | awk -F: '{print $1}' | sort | uniq | xargs sed -i 's/https:\/\/bizport.umeng.com/\/bizport.umeng.com/g'


# 隐藏登陆注册
sed -i 's/header .x-header .nav-menu {/header .x-header .nav-menu { display:none;/g' workbench.umeng.com/public/workbench/um-header.js
sed -i 's/统计/运营/g' mobile.umeng.com/ht/api/v3/menu/newList/relatedId*
sed -i 's/分析/洞察/g' mobile.umeng.com/ht/api/v3/menu/newList/relatedId*
sed -i 's/稳定性//g' mobile.umeng.com/ht/api/v3/menu/newList/relatedId*
sed -i 's/裂变//g' mobile.umeng.com/ht/api/v3/menu/newList/relatedId*

                
grep "<title>TrackingIO" * -R | awk -F: '{print $1}' | sort | uniq | xargs sed -i 's/<title>TrackingIO/<title>昊盟游戏广告智能投放平台/g'
demo.html  $.cookie("ryioDemoapk", "e31caee07ebedf8c172267e73204802f")


grep '"//' * -R | awk -F: '{print $1}' | sort | uniq | xargs sed -i 's/"\/\//"\//g'



# src="//
grep 'src="//' * -R | awk -F: '{print $1}' | sort | uniq | xargs sed -i 's/src="\/\//src="\//g'
# src="https://
grep 'src="https://' * -R | awk -F: '{print $1}' | sort | uniq | xargs sed -i 's/src="https:\/\//src="\//g'
# href="//
grep 'href="//' * -R | awk -F: '{print $1}' | sort | uniq | xargs sed -i 's/href="\/\//href="\//g'
# href="https://
grep 'href="https://' * -R | awk -F: '{print $1}' | sort | uniq | xargs sed -i 's/href="https:\/\//href="\//g'

grep 'https://d1icd6shlvmxi6.cloudfront.net' * -R | awk -F: '{print $1}' | sort | uniq | xargs sed -i 's/https:\/\/d1icd6shlvmxi6.cloudfront.net/\/d1icd6shlvmxi6.cloudfront.net/g'
grep 'https://ssl-player2.720static.com' * -R | awk -F: '{print $1}' | sort | uniq | xargs sed -i 's/https:\/\/ssl-player2.720static.com/\/ssl-player2.720static.com/g'
grep 'https://static.axhub.im' * -R | awk -F: '{print $1}' | sort | uniq | xargs sed -i 's/https:\/\/static.axhub.im/\/static.axhub.im/g'

grep 'https://static.axhub.im' * -R | awk -F: '{print $1}' | sort | uniq | xargs sed -i 's/https:\/\/static.axhub.im/\/static.axhub.im/g'

 https://ssl-player2.720static.com/krp/1.19-pr10/system/piclist.png
