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
								key={entry.start}
								durationInFrames={fps * (entry.end - entry.start)}
							>
								<Images key={index} entry={entry} />;
							</TransitionSeries.Sequence>
							<TransitionSeries.Transition
								presentation={slide('from-left')}
								timing={linearTiming({
									durationInFrames: 2,
									easing: Easing.bezier(0.02, 1.85, 0.83, 0.43),
								})}
							/>
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
		durationInFrames: durationInFrames,
	});

	const zoom = interpolate(spr, [0, 0.5, 1], [1, 1.2, 1.1], {
		easing: Easing.bezier(0.23, 1, 0.32, 1),
		// extrapolateLeft: 'clamp',
		// extrapolateRight: 'clamp',
	});

	const blur = interpolate(
		initialSpring,
		[0.0, 0.09, 0.99, 0.995, 1],
		[20, 0, 0, 0, 5],
		{
			easing: Easing.bezier(0.23, 1, 0.32, 1),
			extrapolateLeft: 'identity',
			extrapolateRight: 'identity',
		}
	);

	return (
		<>
			<svg xmlns="http://www.w3.org/2000/svg" version="1.1" className="filters">
				<defs>
					<filter id="blur">
						<feGaussianBlur in="SourceGraphic" stdDeviation={`${blur * 5},0`} />
					</filter>
				</defs>
			</svg>
			<Img
				style={{
					transform: ` scale(${zoom}) ${
						initialSpring > 0.99
							? `translateX(${blur * 5}px)`
							: `translateX(-${blur * 5}px)`
					}`,
					filter: `url(#blur)`,
					objectPosition: 'center',
					objectFit: 'cover',

					position: 'absolute',
					top: '50%', // Center vertically
					left: '50%', // Center horizontally
					transform: 'translate(-50%, -50%)',
					// zIndex: 150,
					// height: '100vh',
					width: 1080,
					height: 1920,
					// transformOrigin: 'center center', // Move rotation origin to the
					// opacity: 0.1
					// transform: `translateX(-${blur * 5}px)`,
					// transition: 'all 5s ease',
				}}
				src={staticFile(entry.name)}
			/>
		</>
	);
};
