import streamlit as st
from PIL import Image, ImageDraw
import qrcode, io, zipfile, random

st.title("🛂 Bulk Specimen Travel Document Generator")
st.caption("FOR EDUCATIONAL CLASS PROJECT ONLY")

names = ["SPACEMAN", "ALPHA DEV", "BETA TEST", "GAMMA UI", "DELTA AI",
         "OMEGA CODE", "PIXEL PRO", "DATA WIZ", "WEB NINJA", "CLOUD KID"]

def create_specimen_doc(name, doc_no):
    img = Image.new("RGB", (900, 600), (250, 250, 250))
    draw = ImageDraw.Draw(img)
    
    # Header - clearly NOT a government
    draw.rectangle([(0,0),(900,100)], fill=(10, 50, 100))
    draw.text((450,35), "SPECIMEN TRAVEL DOCUMENT", fill="white", anchor="mm")
    draw.text((450,70), "ISSUED BY: CLASS PROJECT AUTHORITY", fill="yellow", anchor="mm")
    
    # Photo
    draw.rectangle([(50,150),(250,350)], outline="black", width=2)
    draw.text((150,250), "PHOTO", fill="gray", anchor="mm")
    
    # Fields - same structure as passport but fake
    draw.text((300,160), f"Full Name: {name}")
    draw.text((300,190), f"Document No: {doc_no}")
    draw.text((300,220), f"Nationality: PROJECT LAND")
    draw.text((300,250), f"Date of Birth: {random.randint(1995,2005)}/01/01")
    draw.text((300,280), f"Place of Issue: CLASS ROOM")
    draw.text((300,310), f"Date of Issue: 01 JAN 2025")
    draw.text((300,340), f"Date of Expiry: 01 JAN 2030")
    
    # MRZ - for coding practice
    mrz1 = f"P<SPC<{name.replace(' ','<<')}<<<<<<<<<<<<<<<<<<<<<<"
    mrz2 = f"{doc_no}<SPC<950101<M<300101<<<<<<<<<<<<<<00"
    draw.rectangle([(50,400),(850,470)], fill="white")
    draw.text((60,415), mrz1)
    draw.text((60,445), mrz2)
    
    # Big watermark
    draw.text((450,550), "SPECIMEN - FOR EDUCATIONAL USE ONLY", fill="red", anchor="mm")
    
    # QR
    qr = qrcode.QRCode(box_size=3).make_image()
    img.paste(qr, (780, 480))
    return img

if st.button("🚀 Generate 10 Specimen Documents"):
    zip_buf = io.BytesIO()
    with zipfile.ZipFile(zip_buf, "w") as z:
        for i,name in enumerate(names):
            doc = create_specimen_doc(name, f"P2025{i+1:03}")
            buf = io.BytesIO()
            doc.save(buf, format="PNG")
            z.writestr(f"specimen_doc_{i+1}.png", buf.getvalue())
    st.download_button("📥 Download 10 Documents ZIP", zip_buf.getvalue(), "specimen_docs.zip")
