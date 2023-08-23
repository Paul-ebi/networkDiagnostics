#!/usr/bin/env python
# coding: utf-8

# In[6]:


import subprocess
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO
import speedtest
import signal


def run_ping(destination, packet_count):
    try:
        ping_output = subprocess.check_output(["ping", "-n", str(packet_count), destination], universal_newlines=True)
        return ping_output
    except subprocess.CalledProcessError as e:
        return f"Ping failed with error:\n{e}"

def run_traceroute(destination):
    try:
        traceroute_output = subprocess.check_output(["tracert", destination], universal_newlines=True)
        return traceroute_output
    except subprocess.CalledProcessError as e:
        return f"Traceroute failed with error:\n{e}"

def run_speedtest():
    def handler(signum, frame):
        raise Exception("Speed test interrupted")

    signal.signal(signal.SIGINT, handler)

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

    # Ping Results
    story.append(Spacer(1, 20))
    story.append(Paragraph("Ping Results:", styles['Heading2']))
    ping_lines = ping_results.splitlines()
    for line in ping_lines:
        story.append(Paragraph(line, styles['Normal']))

    # Traceroute Results
    story.append(Spacer(1, 20))
    story.append(Paragraph("Traceroute Results:", styles['Heading2']))
    traceroute_lines = traceroute_results.splitlines()
    for line in traceroute_lines:
        story.append(Paragraph(line, styles['Normal']))

    # SpeedTest Results
    story.append(Spacer(1, 20))
    story.append(Paragraph("SpeedTest Results:", styles['Heading2']))
    speed_lines = speed_results.splitlines()
    for line in speed_lines:
        story.append(Paragraph(line, styles['Normal']))

    doc.build(story)
    
    buffer.seek(0)
    return buffer

def main():
    destinations = ['8.8.8.8', 'c2.td.commpeak.com', '116.202.64.40']
    packet_count = 100

    ping_results = ""
    traceroute_results = ""
    speed_results = ""
    
    
    speed_results = run_speedtest()

    for dest in destinations:
        ping_results += f"\nPing to {dest}:\n"
        ping_results += run_ping(dest, packet_count)

        traceroute_results += f"\nTraceroute to {dest}:\n"
        traceroute_results += run_traceroute(dest)
        

    pdf_buffer = create_pdf_report(ping_results, traceroute_results, speed_results)
    print("networkDiagx is running in Background..\nPlease Hold on!")
    
    with open("network_report.pdf", "wb") as pdf_file:
        pdf_file.write(pdf_buffer.getvalue())  # Use getvalue() to retrieve the content of BytesIO
        print("PDF report generated: network_report.pdf")

if __name__ == "__main__":
    main()


# In[ ]:





# In[ ]:




