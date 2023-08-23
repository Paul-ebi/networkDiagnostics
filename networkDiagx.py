#!/usr/bin/env python
# coding: utf-8

# In[7]:


print("networkDiagx is running in Background..\nPlease Hold on!")
import subprocess
import speedtest
import signal
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO

def run_ping(destination, packet_count):
    try:
        ping_output = subprocess.check_output(["ping", "-n", str(packet_count), destination], universal_newlines=True)
        summary_lines = []
        summary_started = False

        for line in ping_output.splitlines():
            if "Ping statistics" in line:
                summary_started = True
                summary_lines.append(line)
            elif summary_started:
                if line.strip() == "":
                    break
                summary_lines.append(line)

        return "\n".join(summary_lines)
    except subprocess.CalledProcessError as e:
        return f"Ping failed with error:\n{e}"


def run_traceroute(destination):
    try:
        traceroute_output = subprocess.check_output(["tracert", destination], universal_newlines=True)
        return traceroute_output
    except subprocess.CalledProcessError as e:
        return f"Traceroute failed with error:\n{e}"

def run_speedtest():
    signal.signal(signal.SIGINT, signal.SIG_IGN)  # Ignore the interrupt signal
    try:
        st = speedtest.Speedtest()
        st.get_best_server()
        download_speed = st.download() / 1024 / 1024  # Convert to Mbps
        upload_speed = st.upload() / 1024 / 1024  # Convert to Mbps
        return f"Download Speed: {download_speed:.2f} Mbps\nUpload Speed: {upload_speed:.2f} Mbps"
    except Exception as e:
        return f"Speed test failed with error:\n{e}"

def create_pdf_report(ping_results, traceroute_results, speed_results):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()

    story = []
    story.append(Paragraph("Network Diagnostics Report", styles['Title']))

    for title, content in [("Ping Results:", ping_results), ("Traceroute Results:", traceroute_results), ("SpeedTest Results:", speed_results)]:
        story.append(Spacer(1, 20))
        story.append(Paragraph(title, styles['Heading2']))
        content_paragraphs = content.strip().split('\n')
        for line in content_paragraphs:
            story.append(Paragraph(line, styles['Normal']))

    doc.build(story)
    buffer.seek(0)
    return buffer

# ... (other imports and functions)

def main():
    destinations = ['8.8.8.8', 'xx.xx.xxxxx.com', 'xxx.xxx.xx.xx']
    packet_count = 100  # Reduced packet count for clarity

    ping_results = ""
    traceroute_results = ""
    speed_results = run_speedtest()

    for dest in destinations:
        ping_results += f"<b>Ping to {dest}:</b>\n"
        ping_results += run_ping(dest, packet_count)
        ping_results += "\n\n"  # Add two new lines after each destination

        traceroute_results += f"<b>Traceroute to {dest}:</b>\n"
        traceroute_results += run_traceroute(dest)
        traceroute_results += "\n\n"  # Add two new lines after each destination

    pdf_buffer = create_pdf_report(ping_results, traceroute_results, speed_results)


    with open("network_report.pdf", "wb") as pdf_file:
        pdf_file.write(pdf_buffer.getvalue())
        print("PDF report generated: network_report.pdf")

if __name__ == "__main__":
    main()


# In[ ]:





# In[ ]:




