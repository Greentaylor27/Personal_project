import React, { useState } from "react";

export default function MomentumTracker() {
  const MIN = -6;
  const MAX = 10;
  const [momentum, setMomentum] = useState(2);
  const [maxMomentum, setMaxMomentum] = useState(10);

  const increment = () => {
    if (momentum < maxMomentum) setMaxMomentum(momentum + 1);
  };

  const decrement = () => {
    if (momentum > MIN) setMomentum(momentum - 1);
  };

  const reset = () => setMomentum(2);

  return (
    <div className="flex flex-col items-center bg-neutral-500 text-white rounded-2xl p-4 shadow-lg">
      <h2 className="text-lg font-semibold mb-2">Momentum</h2>

      <div className="flex flex-col items-center space-y-1 my-2">
        {[...Array(MAX - MIN + 1)].map((_, i) => {
          const value = MAX - i;
          const isActive = value === momentum;
          return (
            <div
              key={value}
              className={`w-16 text-center rounded-md py-1 cursor-pointer ${
                isActive
                  ? "bg-emerald-500 font-bold text-black"
                  : "bg-neutral-700 hover:bg-neutral-600"
              }`}
              onClick={() => setMomentum(value)}
              >
                {value > 0 ? `+${value}` : value}
              </div>
          );
        })}
      </div>

      <div className="flex justify-center w-full mt-2">
        <button
          onClick={decrement}
          className="px-2 py-1 bg-neutral-700 rounded hover:bg-neutral-600"
        >
          -
        </button>

        <button
          onClick={reset}
          className="px-2 py-1 bg-amber-500 text-neutral-500 rounded hover:bg-amber-400"
        >
          Reset
        </button>

        <button
          onClick={increment}
          className="px-2 py-1 bg-neutral-700 rounded hover:bg-neutral-600"
        >
          +
        </button>
      </div>
    </div>
  );
}


