import {Series} from 'remotion';
import React from 'react';
import {staticFile, useVideoConfig, Img} from 'remotion';
import {slide} from '@remotion/transitions/slide';
import imageSequences from './Assets/ImageSequences.json';
import {TransitionSeries, linearTiming} from '@remotion/transitions';
export default function ImageStream() {
	const {fps} = useVideoConfig();
	return (
		<TransitionSeries
			style={{
				color: 'white',
				position: 'absolute',
				zIndex: 0,
				objectFit: 'cover',
			}}
		>
			{imageSequences.map((entry, index) => {
				return (
					<TransitionSeries.Sequence
						key={index}
						from={fps * entry.start}
						durationInFrames={fps * (entry.end - entry.start)}
					>
						<Img className="zoomInOut" src={staticFile(entry.name)} />
					</TransitionSeries.Sequence>
				);
			})}
		</TransitionSeries>
	);
}
