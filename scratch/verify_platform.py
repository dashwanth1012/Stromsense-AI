import requests
import sys

sys.stdout.reconfigure(encoding='utf-8')

def test_export():
    print("Testing /cwc/export/analysis CSV generation...")
    url = (
        "http://127.0.0.1:8000/cwc/export/analysis"
        "?date=2025-04-12"
        "&station=Visakhapatnam"
        "&format=csv"
        "&verdict=APPROVED_IMD_REPRODUCTION_VERIFIED"
        "&reviewer_id=IMD-MET-CWC-431"
        "&comments=Convective%20forcing%20and%20buoyancy%20parameters%20aligned%20perfectly."
        "&timestamp=2026-06-03%2011:46:23"
    )
    try:
        r = requests.get(url)
        if r.status_code == 200:
            print("Export API Success!")
            content = r.text
            print("Exported Content Preview:")
            for line in content.splitlines()[:35]:
                print("  ", line)
            
            # Check for the reviewer metadata
            assert "Reviewer Verdict" in content, "Reviewer Verdict missing from CSV!"
            assert "Reviewer ID / Docket" in content, "Reviewer ID missing from CSV!"
            assert "Reviewer Comments" in content, "Reviewer Comments missing from CSV!"
            assert "Signature Timestamp" in content, "Signature Timestamp missing from CSV!"
            print("\n✓ CSV Export Verification Passed successfully!")
        else:
            print(f"Export API failed with status code {r.status_code}: {r.text}")
            sys.exit(1)
    except Exception as e:
        print("Error during export request:", e)
        sys.exit(1)

if __name__ == "__main__":
    test_export()
