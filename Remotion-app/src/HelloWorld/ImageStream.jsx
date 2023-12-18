import {
	AbsoluteFill,
	Series,
	interpolate,
	spring,
	useCurrentFrame,
} from 'remotion';
import React from 'react';
import {staticFile, useVideoConfig, Img, Easing} from 'remotion';
import imageSequences from './Assets/ImageSequences.json';
import {TransitionSeries, linearTiming} from '@remotion/transitions';
import {slide} from '@remotion/transitions/slide';
export default function ImageStream() {
	const {fps} = useVideoConfig();

	return (
		<AbsoluteFill
			style={{
				top: '50%',
				left: '50%',
				transform: 'translate(-50%, -50%)',
				color: 'white',
				position: 'absolute',
				width: '100%',
				height: '100%',
				zIndex: 0,
				objectFit: 'cover',
			}}
		>
			<TransitionSeries>
				{imageSequences.map((entry, index) => {
					return (
						<>
							<TransitionSeries.Sequence
								key={index}
								// from={fps * entry.start}
								durationInFrames={fps * (entry.end - entry.start)}
							>
								<Images key={index} entry={entry} />;
							</TransitionSeries.Sequence>
							<TransitionSeries.Transition
								presentation={slide('from-left')}
								timing={linearTiming({
									durationInFrames: 1,
									easing: Easing.bezier(0.02, 1.85, 0.83, 0.43),
								})}
							>
								jelllo
							</TransitionSeries.Transition>
						</>
					);
				})}
			</TransitionSeries>
		</AbsoluteFill>
	);
}

const Images = ({entry, key}) => {
	const {fps} = useVideoConfig();
	const frame = useCurrentFrame();
	const durationInFrames = (entry.end - entry.start) * fps;
	const spr = spring({
		fps,
		frame,
		config: {
			damping: 100,
		},
		delay: 0,
		from: 0,
		to: 1,
		durationInFrames: durationInFrames,
	});
	const initialSpring = spring({
		fps,
		frame,
		config: {
			damping: 100,
		},
		delay: 0,
		from: 0,
		to: 1,
		durationInFrames: 2,
	});

	const zoom = interpolate(spr, [0, 0.5, 1], [1, 1.5, 1.3], {
		// easing: Easing.bezier(0.8, 0.22, 0.96, 0.65),
		extrapolateLeft: 'clamp',
		extrapolateRight: 'clamp',
	});

	const blur = interpolate(initialSpring, [0, 1], [30, 0], {
		// easing: Easing.bezier(0.8, 0.22, 0.96, 0.65),
		extrapolateLeft: 'clamp',
		extrapolateRight: 'clamp',
	});

	return (
		<>
			<Img
				style={{
					transform: `scale(${zoom})`,
					filter: `blur(${blur}px)`,
					transform: `translateX((${blur * 10}px)`,
					// transition: 'all 5s ease',
				}}
				src={staticFile(entry.name)}
			/>
		</>
	);
};
