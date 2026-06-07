import React from "react";

export default class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true };
  }

  componentDidCatch(error, errorInfo) {
    console.error("ErrorBoundary caught an error:", error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return (
        <div style={{
          padding: "24px",
          backgroundColor: "#1e1b4b",
          border: "2px dashed #f43f5e",
          borderRadius: "12px",
          color: "#f43f5e",
          fontFamily: "JetBrains Mono",
          textAlign: "center",
          margin: "20px"
        }}>
          <h3 style={{ margin: "0 0 8px 0", fontSize: "16px" }}>⚠ MODULE FAILED TO LOAD</h3>
          <p style={{ margin: 0, fontSize: "12px", color: "#fda4af" }}>
            An unexpected error occurred during rendering. Please check connection and retry.
          </p>
        </div>
      );
    }

    return this.props.children;
  }
}
