[app]
# APP在手机桌面显示的名字
title = 个人记账本
# 包名，小写字母，不要中文
package.name = accountbook
package.domain = org.accountbook

source.dir = .
source.include_exts = py,png,jpg,ttf

# 版本号
version = 0.1

requirements = python3,kivy

android.api = 33
android.ndk = 25b
android.sdk = 24
android.archs = arm64-v8a

android.permissions = ACCESS_NETWORK_STATE
android.orientation = portrait
android.allow_backup = True

# 把字体打包进APK，你的字体文件名如果不是simhei.ttf，记得改成对应名字
android.add_assets = simhei.ttf
