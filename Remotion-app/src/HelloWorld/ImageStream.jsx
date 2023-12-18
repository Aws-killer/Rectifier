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

	const frame = useCurrentFrame();
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
					const durationInFrames = (entry.end - entry.start) * fps;

					const zoom = interpolate(
						frame,
						[
							fps * entry.start,
							fps * entry.start + durationInFrames / 2,
							fps * entry.end,
						],
						[1, 1.5, 1.3],
						[1, 1.2, 1]
					);

					return (
						<>
							<TransitionSeries.Sequence
								key={index}
								// from={fps * entry.start}
								durationInFrames={fps * (entry.end - entry.start)}
							>
								<Img
									style={{
										transform: `scale(${zoom})`,
									}}
									src={staticFile(entry.name)}
								/>
							</TransitionSeries.Sequence>
							<TransitionSeries.Transition
								presentation={slide('from-left')}
								timing={linearTiming({
									durationInFrames: 1,
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
