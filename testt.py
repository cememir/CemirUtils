from cemirutils import CemirUtilsEmail

# Kullanım
email_util = CemirUtilsEmail(
    smtp_host="smtp.gmail.com",
    smtp_port=465,
    smtp_user="musluyuksektepe@gmail.com",
    smtp_pass="nopass",
    smtp_ssl=True
)

email_util.send_email(
    to_email="cememir2017@gmail.com",
    subject="Test Subject",
    body_html="<html><body><h1>This is a test email in HTML.</h1></body></html>",
    attachments=["2024.pdf", "not_found.log"],
    zip_files=False  # Dosyaları zipleyip eklemek için
)
