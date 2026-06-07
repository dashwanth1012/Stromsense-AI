function Sidebar({ activeSection, setActiveSection }) {

  const menuItems = [

    "Dashboard",
    "Analytics",
    "Radar",
    "Prediction",
    "Alerts",
    "Research"

  ];

  return (

    <div
      style={{
        width: "260px",
        background:
          "linear-gradient(to bottom,#081120,#0d1729)",
        height: "100vh",
        position: "fixed",
        left: 0,
        top: 0,
        padding: "30px 20px",
        borderRight: "1px solid #00ffff",
        overflowY: "auto"
      }}
    >

      <h1
        style={{
          color: "#00ffff",
          marginBottom: "40px",
          textAlign: "center",
          fontSize: "30px",
          textShadow: "0 0 20px #00ffff"
        }}
      >
        🌩️ StormSense AI
      </h1>

      {
        menuItems.map((item) => (

          <div
            key={item}

            onClick={() =>
              setActiveSection(item)
            }

            style={{
              padding: "18px",
              marginBottom: "15px",
              borderRadius: "14px",
              cursor: "pointer",
              transition: "0.3s",
              fontWeight: "bold",

              background:
                activeSection === item
                  ? "#00ffff"
                  : "#10192f",

              color:
                activeSection === item
                  ? "#000"
                  : "#fff",

              boxShadow:
                activeSection === item
                  ? "0 0 20px #00ffff"
                  : "none"
            }}
          >

            {item}

          </div>

        ))
      }

    </div>

  );

}

export default Sidebar;