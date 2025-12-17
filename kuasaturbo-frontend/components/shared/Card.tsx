import React from "react";

interface CardProps {
  children: React.ReactNode;
  className?: string;
}

export default function Card({ children, className = "" }: CardProps) {
  return (
    <div
      className={`rounded-xl shadow-sm border border-slate-200 p-6 bg-white ${className}`}
    >
      {children}
    </div>
  );
}
