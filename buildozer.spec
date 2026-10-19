[app]

package.name = accountbook
package.domain = org.accountbook
source.dir = .
source.include_exts = py,png,jpg,ttf,json

requirements = python3,kivy

orientation = portrait
os.android = True

package.version = 0.1
android.api = 33
android.ndk = 25b
android.sdk = 24
android.archs = arm64-v8a

# 权限
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
