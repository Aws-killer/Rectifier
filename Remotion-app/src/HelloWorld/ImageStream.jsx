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

export default function ImageStream() {
	const {fps} = useVideoConfig();

	const frame = useCurrentFrame();
	return (
		<AbsoluteFill>
			<TransitionSeries
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
						{
							// easing: Easing.bezier(0.8, 0.22, 0.96, 0.65),
							extrapolateLeft: 'clamp',
							extrapolateRight: 'clamp',
						}
					);

					return (
						<TransitionSeries.Sequence
							key={index}
							from={fps * entry.start}
							durationInFrames={fps * (entry.end - entry.start)}
						>
							<Img
								style={{
									transform: `scale(${zoom})`,
									// transition: 'all 5s ease',
								}}
								src={staticFile(entry.name)}
							/>
						</TransitionSeries.Sequence>
					);
				})}
			</TransitionSeries>
		</AbsoluteFill>
	);
}
