import os
import random
import time
import instaloader
import undetected_chromedriver as uc


# تسجيل الدخول بـ instaloader (فقط لتحميل لاحقًا أو إدارة الجلسة)
L = instaloader.Instaloader()
USERNAME = '1.million.11'
L.load_session_from_file(USERNAME)

# إعداد Selenium بدون واجهة
options = uc.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
driver = uc.Chrome(options=options)


# الحساب المستهدف
#target_username = input("🧾 أدخل اسم الحساب (بدون @): ")
url = f"https://www.instagram.com/one_billion_academy/reels/"

print(f"\n🔍 فتح الصفحة: {url}")
driver.get(url)
time.sleep(5)

# تمرير الصفحة لتحميل الريلزات
for _ in range(4):  # عدل العدد حسب عدد الريلزات المطلوب
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)

# استخراج روابط الريلز
elements = driver.find_elements("xpath", '//a[contains(@href, "/reel/")]')
reel_links = list(set([el.get_attribute('href') for el in elements]))  # إزالة التكرار

driver.quit()

# ترتيب عشوائي للروابط
random.shuffle(reel_links)

# مجلد التحميل
download_dir = "INSTA"
os.makedirs(download_dir, exist_ok=True)

# تحميل الريلز باستخدام Instaloader
count = 0
for reel_url in reel_links:
    shortcode = reel_url.split("/reel/")[1].strip("/")
    try:
        post = instaloader.Post.from_shortcode(L.context, shortcode)
        filename = os.path.join(download_dir, f"{shortcode}.mp4")
        if not os.path.exists(filename):  # التحقق من عدم التكرار
            print(f"⬇️ تحميل: {reel_url}")
            L.download_post(post, target=download_dir)
            count += 1
        else:
            print(f"⏩ تم تخطي الريلز (مكرر): {shortcode}")
    except Exception as e:
        print(f"❌ فشل في تحميل: {reel_url}\nسبب: {e}")

print(f"\n✅ تم تحميل {count} ريلز في مجلد {download_dir}")
