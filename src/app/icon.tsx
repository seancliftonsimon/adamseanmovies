import { ImageResponse } from "next/og";

export const size = {
  width: 512,
  height: 512,
};

export const contentType = "image/png";

export default function Icon() {
  return new ImageResponse(
    (
      <div
        style={{
          display: "flex",
          height: "100%",
          width: "100%",
          alignItems: "center",
          justifyContent: "center",
          background:
            "linear-gradient(180deg, rgb(44, 105, 216) 0%, rgb(0, 51, 153) 100%)",
          color: "rgb(242, 228, 0)",
          fontSize: 160,
          fontWeight: 900,
          letterSpacing: "-0.08em",
          position: "relative",
        }}
      >
        <div
          style={{
            position: "absolute",
            inset: 28,
            border: "18px solid rgb(17, 17, 17)",
            borderRadius: 28,
            display: "flex",
          }}
        />
        <div
          style={{
            position: "absolute",
            top: 76,
            left: 76,
            right: 76,
            bottom: 76,
            border: "12px solid rgb(242, 228, 0)",
            borderRadius: 22,
            display: "flex",
          }}
        />
        <span style={{ display: "flex" }}>📼</span>
      </div>
    ),
    size,
  );
}
