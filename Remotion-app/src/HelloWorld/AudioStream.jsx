import {Series} from 'remotion';
import React from 'react';
import {staticFile, useVideoConfig, Audio} from 'remotion';
import audioSequences from './Assets/AudioSequences.json';
import {TransitionSeries} from '@remotion/transitions';
export default function AudioStream() {
	const {fps} = useVideoConfig();
	return (
		<TransitionSeries>
			{audioSequences.map((entry, index) => {
				return (
					<Audio
						volume={entry.props.volume}
						endAt={entry.props.endAt}
						startFrom={entry.props.startFrom}
						src={staticFile(entry.name)}
					/>
				);
			})}
		</TransitionSeries>
	);
}
