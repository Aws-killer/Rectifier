import { useGsapTimeline } from '../../lib/useGsapTimeline'
import { AbsoluteFill } from 'remotion';
import gsap from 'gsap';



export default function GsapAnimation({ Timeline, style, className, children, plugins = [] }) {
  gsap.registerPlugin(...plugins);
  const ContainerRef = useGsapTimeline(Timeline);
  return (
    <AbsoluteFill className={className} style={style} ref={ContainerRef}>
      {children}
    </AbsoluteFill>
  );
}
