import {Series, interpolate, spring, useCurrentFrame} from 'remotion';
import React from 'react';
import {staticFile, useVideoConfig, Img} from 'remotion';
import {slide} from '@remotion/transitions/slide';
import imageSequences from './Assets/ImageSequences.json';
import {TransitionSeries, linearTiming} from '@remotion/transitions';

export default function ImageStream() {
	const {fps} = useVideoConfig();

	const frame = useCurrentFrame();
	return (
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
					[0, frame + 2 * (durationInFrames / 4), frame + durationInFrames],
					[1, 1.2, 1],
					{extrapolateRight: 'clamp'}
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
								transition: 'all 1s ease',
							}}
							src={staticFile(entry.name)}
						/>
					</TransitionSeries.Sequence>
				);
			})}
		</TransitionSeries>
	);
}
