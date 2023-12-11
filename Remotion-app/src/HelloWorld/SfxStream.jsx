import {Series} from 'remotion';
import React from 'react';
import {staticFile, useVideoConfig, Audio} from 'remotion';
import sfxSequences from './Assets/SfxSequences.json';
import {TransitionSeries} from '@remotion/transitions';
export default function SfxStream() {
	const {fps} = useVideoConfig();
	return (
		<TransitionSeries>
			{sfxSequences.map((entry, index) => {
				return (
					<TransitionSeries.Sequence
						key={index}
						from={fps * entry.start}
						durationInFrames={30}
					>
						<Audio
							volume={entry.props.volume}
							// endAt={entry.props.endAt}
							startFrom={entry.props.startFrom}
							src={staticFile(entry.name)}
						/>
					</TransitionSeries.Sequence>
				);
			})}
		</TransitionSeries>
	);
}
