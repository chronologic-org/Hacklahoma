const colors = [
    "#FBF8CC",
    "#FDE4CF",
    "#FFCFD2",
    "#F1C0E8",
    "#CFBAF0",
    "#A3C4F3",
    "#90DBF4",
    "#8EECF5",
    "#98F5E1",
    "#B9FBC0",
  ]
  
  const ColorWave2D: React.FC = () => {
    return (
      <div className="wave-container">
        <div className="wave"></div>
        <style jsx>{`
          .wave-container {
            width: 100%;
            height: 300px;
            overflow: hidden;
            position: relative;
          }
          .wave {
            position: absolute;
            top: -100%;
            left: -100%;
            width: 200%;
            height: 200%;
            background-color: ${colors[0]};
            background-image: linear-gradient(
              45deg,
              ${colors
                .map(
                  (color, index) =>
                    `${color} ${index * 10}%, ${colors[(index + 1) % colors.length]} ${(index + 1) * 10}%`,
                )
                .join(", ")}
            );
            animation: wave 10s linear infinite;
          }
          @keyframes wave {
            0% {
              transform: rotate(0deg);
            }
            100% {
              transform: rotate(360deg);
            }
          }
        `}</style>
      </div>
    )
  }
  
  export default ColorWave2D