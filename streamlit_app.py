import React, { useState, useRef, useEffect } from 'react';

const PhotoCard = () => {
  const [frontImage, setFrontImage] = useState("/api/placeholder/240/320");
  const [backImage, setBackImage] = useState("/api/placeholder/240/320");
  const [isFlipped, setIsFlipped] = useState(false);
  const [isAutoRotating, setIsAutoRotating] = useState(false);
  const frameRef = useRef(null);
  const cardRef = useRef(null);
  const lightRef = useRef(null);

  const toggleAutoRotate = (e) => {
    e.stopPropagation(); // Prevent card flip when clicking rotate button
    setIsAutoRotating(!isAutoRotating);
  };

  const handleFrontImageChange = (e) => {
    const file = e.target.files[0];
    if (file && file.type.startsWith('image/')) {
      const reader = new FileReader();
      reader.onload = (e) => setFrontImage(e.target.result);
      reader.readAsDataURL(file);
    }
  };

  const handleBackImageChange = (e) => {
    const file = e.target.files[0];
    if (file && file.type.startsWith('image/')) {
      const reader = new FileReader();
      reader.onload = (e) => setBackImage(e.target.result);
      reader.readAsDataURL(file);
    }
  };

  useEffect(() => {
    const frame = frameRef.current;
    const card = cardRef.current;
    const light = lightRef.current;
    
    const handleMouseMove = (e) => {
      if (isAutoRotating) return; // Disable mouse effect during auto-rotation
      
      const rect = frame.getBoundingClientRect();
      const mouseX = e.clientX - rect.left;
      const mouseY = e.clientY - rect.top;
      const centerX = rect.width / 2;
      const centerY = rect.height / 2;
      
      const percentX = (mouseX - centerX) / centerX;
      const percentY = -((mouseY - centerY) / centerY);
      
      const rotateYValue = isFlipped ? -percentX * 45 : percentX * 45;
      card.style.transform = `${isFlipped ? 'rotateY(180deg)' : 'rotateY(0)'} rotateY(${rotateYValue}deg) rotateX(${percentY * 45}deg)`;
      
      light.style.background = `radial-gradient(circle at ${mouseX}px ${mouseY}px,
        rgba(255, 255, 255, 0.2) 0%,
        rgba(255, 255, 255, 0.1) 20%,
        rgba(255, 255, 255, 0.0) 90%)`;
    };
    
    const handleMouseLeave = () => {
      if (!isAutoRotating) {
        card.style.transform = isFlipped ? 'rotateY(180deg)' : 'rotateY(0)';
        light.style.background = 'none';
      }
    };

    if (frame && card && light) {
      frame.addEventListener('mousemove', handleMouseMove);
      frame.addEventListener('mouseleave', handleMouseLeave);
    }

    return () => {
      if (frame && card && light) {
        frame.removeEventListener('mousemove', handleMouseMove);
        frame.removeEventListener('mouseleave', handleMouseLeave);
      }
    };
  }, [isFlipped, isAutoRotating]);

  const styles = `
    @keyframes autoRotate {
      from {
        transform: rotateZ(10deg) rotateY(0deg);
      }
      to {
        transform: rotateZ(10deg) rotateY(360deg);
      }
    }

    @keyframes glow {
      0% { 
        opacity: 0.6;
        filter: brightness(1);
        transform: scale(1);
      }
      50% { 
        opacity: 1;
        filter: brightness(1.8);
        transform: scale(1.1);
      }
      100% { 
        opacity: 0.6;
        filter: brightness(1);
        transform: scale(1);
      }
    }

    @keyframes pulse {
      0% {
        transform: scale(1);
        opacity: 0.4;
      }
      50% {
        transform: scale(1.4);
        opacity: 0.9;
      }
      100% {
        transform: scale(1);
        opacity: 0.4;
      }
    }

    .frame {
      width: 300px;
      height: 450px;
      transition: transform 200ms;
      perspective: 1000px;
      cursor: pointer;
      z-index: 10;
      position: relative;
    }
    
    .frame:hover {
      transform: scale3d(1.05, 1.05, 1.05);
    }
    
    .card {
      width: 100%;
      height: 100%;
      position: relative;
      transition: transform 0.8s;
      transform-style: preserve-3d;
    }
    
    .card.flipped {
      transform: rotateY(180deg);
    }

    .card.auto-rotating {
      animation: autoRotate 4s linear infinite;
    }
    
    .front, .back {
      width: 100%;
      height: 100%;
      border-radius: 9px;
      background-position: center;
      background-size: cover;
      background-repeat: no-repeat;
      box-shadow: 0 0 10px 2px rgba(0, 0, 0, 0.1);
      position: absolute;
      backface-visibility: hidden;
      -webkit-backface-visibility: hidden;
      transition-duration: 250ms;
      transition-property: transform, box-shadow;
      transition-timing-function: ease-out;
    }
    
    .back {
      transform: rotateY(180deg);
    }
    
    .light {
      position: absolute;
      width: 100%;
      height: 100%;
      border-radius: 9px;
      pointer-events: none;
    }
  `;

  const holographicOverlayStyle = {
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    background: `
      linear-gradient(45deg, 
        transparent 20%, 
        rgba(192,192,192,0.7) 30%, 
        transparent 40%
      ),
      linear-gradient(135deg,
        transparent 30%, 
        rgba(169,169,169,0.7) 40%, 
        transparent 50%
      ),
      linear-gradient(225deg,
        transparent 40%, 
        rgba(211,211,211,0.7) 50%, 
        transparent 60%
      ),
      linear-gradient(315deg,
        transparent 50%, 
        rgba(192,192,192,0.7) 60%, 
        transparent 70%
      )
    `,
    backgroundSize: '400% 400%, 400% 400%, 400% 400%, 400% 400%',
    borderRadius: '9px',
    pointerEvents: 'none',
    mixBlendMode: 'overlay'
  };

  return (
    <div className="relative flex flex-col items-center justify-center gap-16 w-full min-h-screen bg-gray-950">
      <style>{styles}</style>
      
      {/* Base gradient background */}
      <div className="absolute inset-0 bg-gradient-to-br from-gray-950 via-gray-900 to-gray-950"></div>
      
      {/* Central glowing effects */}
      <div className="absolute inset-0" 
           style={{
             background: 'radial-gradient(circle at center, rgba(147, 197, 253, 0.4) 0%, rgba(147, 197, 253, 0.2) 30%, transparent 70%, transparent 100%)',
             animation: 'glow 4s infinite ease-in-out'
           }}></div>
      <div className="absolute inset-0" 
           style={{
             background: 'radial-gradient(circle at center, rgba(59, 130, 246, 0.5) 0%, rgba(59, 130, 246, 0.3) 20%, transparent 60%, transparent 100%)',
             animation: 'pulse 6s infinite ease-in-out'
           }}></div>
      <div className="absolute inset-0" 
           style={{
             background: 'radial-gradient(circle at center, rgba(255, 255, 255, 0.3) 0%, rgba(255, 255, 255, 0.1) 10%, transparent 50%, transparent 100%)',
             animation: 'pulse 4s infinite ease-in-out'
           }}></div>

      {/* File upload buttons and rotation button */}
      <div className="absolute top-4 left-4 flex gap-2 z-20">
        <label className="px-3 py-1 bg-blue-500/20 hover:bg-blue-500/30 rounded-full text-xs text-white cursor-pointer transition-colors">
          Front
          <input
            type="file"
            accept="image/*"
            onChange={handleFrontImageChange}
            className="hidden"
          />
        </label>
        <label className="px-3 py-1 bg-blue-500/20 hover:bg-blue-500/30 rounded-full text-xs text-white cursor-pointer transition-colors">
          Back
          <input
            type="file"
            accept="image/*"
            onChange={handleBackImageChange}
            className="hidden"
          />
        </label>
        <button
          onClick={toggleAutoRotate}
          className={`px-3 py-1 rounded-full text-xs text-white cursor-pointer transition-colors ${
            isAutoRotating 
              ? 'bg-blue-500 hover:bg-blue-600'
              : 'bg-blue-500/20 hover:bg-blue-500/30'
          }`}
        >
          {isAutoRotating ? 'Stop Rotation' : 'Start Rotation'}
        </button>
      </div>

      {/* 3D Card */}
      <div 
        className="frame" 
        ref={frameRef} 
        onClick={() => !isAutoRotating && setIsFlipped(!isFlipped)}
      >
        <div 
          className={`card ${isFlipped ? 'flipped' : ''} ${isAutoRotating ? 'auto-rotating' : ''}`}
          ref={cardRef}
        >
          <div 
            className="front"
            style={{
              backgroundImage: `url(${frontImage})`
            }}
          >
            <div className="light" ref={lightRef}></div>
            <div style={holographicOverlayStyle}></div>
          </div>
          <div 
            className="back"
            style={{
              backgroundImage: `url(${backImage})`
            }}
          >
            <div className="light"></div>
            <div style={holographicOverlayStyle}></div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default PhotoCard;
