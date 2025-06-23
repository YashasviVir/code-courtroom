import { cn } from "@/lib/utils";
import React from "react";

interface AgentAvatarProps {
  role: string;
  image: string;
  isActive: boolean;
  className?: string;
}

const AgentAvatar: React.FC<AgentAvatarProps> = ({
  role,
  image,
  isActive,
  className,
}) => {
  return (
    <div className={cn("flex flex-col items-center space-y-1", className)}>
      <div
        className={cn(
          "relative w-12 h-12 rounded-full overflow-hidden border-2 transition-all duration-500",
          isActive
            ? "border-amber-400 shadow-lg shadow-amber-400/50"
            : "border-amber-600/50"
        )}
      >
        <img src={image} alt={role} className="w-full h-full object-cover" />
        {isActive && (
          <>
            {/* Inner glow ring */}
            <div className="absolute inset-0 rounded-full border-2 border-amber-300 animate-pulse" />
            {/* Outer glow effect */}
            <div className="absolute -inset-1 rounded-full bg-amber-400/30 animate-pulse" />
            {/* Expanding glow ring */}
            <div className="absolute -inset-2 rounded-full border border-amber-200/60 animate-ping" />
          </>
        )}
      </div>
      <div className="text-center">
        <h3 className="text-xs font-semibold text-amber-100">{role}</h3>
      </div>
    </div>
  );
};

export default AgentAvatar;
