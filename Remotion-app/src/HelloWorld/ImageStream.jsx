import {Series} from 'remotion';
import React from 'react';
import {staticFile, useVideoConfig, Img} from 'remotion';
import imageSequences from './Assets/ImageSequences.json';
import {TransitionSeries} from '@remotion/transitions';
export default function ImageStream() {
	const {fps} = useVideoConfig();
	return (
		<TransitionSeries
			style={{
				color: 'white',
			}}
		>
			{imageSequences.map((entry, index) => {
				return (
					<TransitionSeries.Sequence
						key={index}
						from={fps * entry.start}
						durationInFrames={fps * (entry.end - entry.start)}
					>
						<Img src={staticFile(entry.name)} />
					</TransitionSeries.Sequence>
				);
			})}
		</TransitionSeries>
	);
}
