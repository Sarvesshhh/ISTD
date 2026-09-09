import os
from html2image import Html2Image

hti = Html2Image()
hti.browser.flags = ['--no-sandbox', '--disable-gpu', '--hide-scrollbars', '--force-device-scale-factor=1']
# Set window size larger to capture full page
hti.custom_flags = ['--window-size=1200,1600']

base_path = 'C:/Users/RAHUL/OneDrive/Desktop/ISTD'
out_path = 'C:/Users/RAHUL/.gemini/antigravity/brain/aa125448-6c1c-4b20-a134-c0f575e022a7'

files = ['index.html', 'about.html', 'events.html', 'office-bearers.html']
out_files = ['index_screenshot.png', 'about_screenshot.png', 'events_screenshot.png', 'office_bearers_screenshot.png']

for f, out_f in zip(files, out_files):
    file_uri = f'file:///{base_path}/{f}'
    out_dest = os.path.join(out_path, out_f)
    print(f"Screenshotting {file_uri} to {out_dest}")
    # hti.screenshot saves in current directory, so we change directory
    os.chdir(out_path)
    hti.screenshot(url=file_uri, save_as=out_f)
    print(f"Saved {out_f}")

print("Done")
