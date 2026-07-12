export default function Logo({ size = 40 }) {
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 100 100"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      aria-label="GYS Logo"
    >
      <circle cx="50" cy="50" r="48" fill="#15803d" />
      <circle cx="50" cy="50" r="42" fill="none" stroke="#f59e0b" strokeWidth="3" />
      <text
        x="50"
        y="66"
        fontSize="46"
        textAnchor="middle"
        fill="#f59e0b"
        fontFamily="Montserrat, sans-serif"
        fontWeight="800"
      >
        G
      </text>
    </svg>
  )
}
