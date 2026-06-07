import { Link } from "react-router-dom";

function Navbar() {

  return (

    <div
      style={{
        background: "#081120",
        padding: "20px 40px",
        display: "flex",
        justifyContent: "space-between",
        alignItems: "center",
        borderBottom: "1px solid #00ffff",
        position: "sticky",
        top: 0,
        zIndex: 999
      }}
    >

      <h1
        style={{
          color: "#00ffff",
          fontSize: "28px",
          textShadow: "0 0 15px #00ffff"
        }}
      >
        🌩️ StormSense AI
      </h1>

      <div
        style={{
          display: "flex",
          gap: "25px"
        }}
      >

        <Link style={linkStyle} to="/">
          Dashboard
        </Link>

        <Link style={linkStyle} to="/radar">
          Radar
        </Link>

        <Link style={linkStyle} to="/analytics">
          Analytics
        </Link>

        <Link style={linkStyle} to="/prediction">
          Prediction
        </Link>

        <Link style={linkStyle} to="/alerts">
          Alerts
        </Link>

        <Link style={linkStyle} to="/research">
          Research
        </Link>

      </div>

    </div>

  );

}

const linkStyle = {

  color: "white",

  textDecoration: "none",

  fontSize: "18px",

  fontWeight: "bold",

  transition: "0.3s"

};

export default Navbar;