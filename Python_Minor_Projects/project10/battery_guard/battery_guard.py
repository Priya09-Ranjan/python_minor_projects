import psutil
import time
import tkinter as tk
from tkinter import messagebox

def show_alert(title, message):
    """Brings warning popup to the very top of the screen."""
    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)
    messagebox.showwarning(title, message)
    root.destroy()

def live_monitor():
    print("=" * 60)
    print(" 🔋 LIVE BATTERY GUARD ACTIVE")
    print("=" * 60)
    print(" 💡 HOW TO STOP THIS PROGRAM:")
    print("    • In IDLE Shell / Terminal: Press [Ctrl + C]")
    print("    • If running as background process: Close Terminal / End Task")
    print("=" * 60 + "\n")
    
    # Track previous state to trigger popup immediately on plug-in
    prev_plugged = None
    full_alert_triggered = False
    low_alert_triggered = False

    while True:
        battery = psutil.sensors_battery()
        
        if battery is None:
            print("❌ Battery sensor not detected.")
            break

        percent = battery.percent
        plugged = battery.power_plugged
        status = "Charging ⚡" if plugged else "Discharging 🔋"

        # Print only when status changes to keep terminal clean
        if plugged != prev_plugged:
            print(f"Status Changed: {percent}% | {status}")

        # --- CASE 1: FULL BATTERY + CHARGER CONNECTED ---
        if percent >= 90 and plugged:
            # Trigger popup if charger was just plugged in OR alert wasn't shown yet
            if not full_alert_triggered or prev_plugged == False:
                print(f"🚨 ALERT TRIGGERED: Battery is {percent}% and plugged in!")
                show_alert(
                    "⚡ Charger Plugged In @ High Battery!", 
                    f"Battery is already at {percent}%!\nPlease UNPLUG the charger to protect battery health."
                )
                full_alert_triggered = True
        else:
            if percent < 85:
                full_alert_triggered = False

        # --- CASE 2: LOW BATTERY + CHARGER DISCONNECTED ---
        if percent <= 20 and not plugged:
            if not low_alert_triggered:
                print(f"🚨 ALERT TRIGGERED: Battery low ({percent}%)!")
                show_alert(
                    "⚠️ Low Battery Warning!", 
                    f"Battery is down to {percent}%!\nPlease CONNECT your charger."
                )
                low_alert_triggered = True
        else:
            if percent > 25:
                low_alert_triggered = False

        # Save state for next iteration
        prev_plugged = plugged
        
        # Checks every 2 seconds for ultra-fast plug-in detection!
        time.sleep(2)

if __name__ == "__main__":
    try:
        live_monitor()
    except KeyboardInterrupt:
        print("\n\n🛑 Battery Guard stopped cleanly. Have a great day! 👋")
