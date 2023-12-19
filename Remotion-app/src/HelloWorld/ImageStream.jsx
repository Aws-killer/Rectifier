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
								<Images entry={entry} />;
							</TransitionSeries.Sequence>
							<TransitionSeries.Transition
								presentation={slide('from-left')}
								timing={linearTiming({
									durationInFrames: 1,
									// easing: Easing.bezier(0.02, 1.85, 0.83, 0.43),
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

const Images = ({entry}) => {
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
		durationInFrames: 0.5 * fps,
	});

	const zoom = interpolate(spr, [0, 0.5, 1], [1, 1.5, 1.3], {
		// easing: Easing.bezier(0.8, 0.22, 0.96, 0.65),
		extrapolateLeft: 'clamp',
		extrapolateRight: 'clamp',
	});

	const blur = interpolate(initialSpring, [0, 1], [30, 0], {
		easing: Easing.bezier(0.23, 1, 0.32, 1),
		extrapolateLeft: 'clamp',
		extrapolateRight: 'clamp',
	});

	return (
		<>
			<div
				style={{
					fontSize: 150,
					position: 'absolute',
					zIndex: 1,
				}}
			>
				{blur}
			</div>

			<Img
				style={{
					transform: `scale(${zoom}) translateX(-${blur * 5}px)`,
					filter: `blur(${blur}px)`,
					// opacity: 0.1
					// transform: `translateX(-${blur * 5}px)`,
					// transition: 'all 5s ease',
				}}
				src={staticFile(entry.name)}
			/>

			{[1, 2, 3, 4, 5, 6, 7, 8, 9, 10].map((i) => {
				return (
					<Img
						key={i}
						style={{
							transform: `scale(${zoom}) translateX(-${blur * i * 5}px)`,
							filter: `blur(${(blur / i) * 2}px)`,
							opacity: 0.1,
							// transform: `translateX(-${blur * 5}px)`,
							// transition: 'all 5s ease',
						}}
						src={staticFile(entry.name)}
					/>
				);
			})}
		</>
	);
};
